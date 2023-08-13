
import json
from .models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

class SignUpView(APIView):
    def post(self, req):
        data = json.loads(req.body)
        userExist = User.objects.filter(username=data["username"])      
        if not userExist:
            serializer = SignUpSerializer(data=data)
            
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    "refresh_token": str(refresh),
                    "access_token": str(refresh.access_token),
                    }
                )
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)
        
        return JsonResponse({"message": "Account already exist"}, status=status.HTTP_400_BAD_REQUEST)

class SignInView(APIView):
    def post(self, req):
        data = json.loads(req.body)  
        serialized_data = LoginSerializer(data=data)
        if serialized_data.is_valid():
            user = serialized_data.validated_data
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token)
            }) 
        return JsonResponse({"message":"Invalid username or password"})
    
class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, req):
        data = json.loads(req.body)
        serializer = ProductSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Product has been added"}, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, req):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True).data
        return JsonResponse(serializer, safe=False)

class ProductReview(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, req, product_id):
        product = Product.objects.filter(id = product_id).first()
        if product:
            reviews = Review.objects.filter(product = product.id).values("id","user","rate","review","active") #convert into dict reviews
            serializer = ProductSerializer(product).data
            serializer["reviews"] = list(reviews)
            return JsonResponse(serializer, safe=False)
        else:
            return JsonResponse({"message":"Product not found"})
    
    def post(self, req, product_id):
        data = json.loads(req.body)
        data["product"]=product_id
        data["user"]=req.user.id
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Review has been added", "data": data}, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Search a product by name and pageno
class ProductSearch(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, req):
        name = req.GET.get("name","")
        page_number = req.GET.get("page", 1)
        products = Product.objects.filter(name__icontains = name)
        
        paginator = Paginator(products, 5)
        page = paginator.get_page(page_number)
        product_pages = page.object_list
        
        serialized_products = ProductSerializer(product_pages, many=True).data
        return JsonResponse({
            "data": serialized_products,
            "total_pages": paginator.num_pages,
            "total_products": products.count()
        }, safe=False)
    
#Filter products within specific price range
class ProductsByPrice(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, req):
        minPrice = req.GET.get('min')
        maxPrice = req.GET.get('max')
        if minPrice and maxPrice:
            products = Product.objects.filter(Q(price__gte = minPrice) & Q(price__lte=maxPrice))  
            responses = [{
                "name": product.name,
                "brand": product.brand,
                "description": product.description,
                "category": product.category,
                "price": product.price
            } for product in products]
        
        return JsonResponse(responses, safe=False)


#Filter products by category, brand and active          
class ProductsFilterByCategoryBrandActive(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, req):
        category = req.GET.get("category", None)
        brand = req.GET.get("brand", None)
        active = req.GET.get("active", None)
        products = Product.objects.all()
        
        if category:
            products = products.filter(category__iexact = category)
        if brand:
            products = products.filter(brand__iexact = brand)
        if active:
            products = products.filter(active__in = [bool(int(active))])
        
        # serialized_products = ProductSerializer(products, many=True).data
        # return JsonResponse(serialized_products, safe=False)
           
        context = [{
            "product_id": product.id,
            "name": product.name,
            "category": product.category,
            "brand": product.brand,
            "active": product.active
        } for product in products]
        
        return JsonResponse(context, safe=False)


#Filter products by name or descriptions
class ProductsByNameDesc(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        else:
            return []
    
    # "$match" operator in mongodb is similar to "__icontains" in django
    def get(self, req):
        query = req.GET.get("query", None)
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains = query))
        serialized_products = ProductSerializer(products, many=True).data
        return JsonResponse(serialized_products, safe=False)
    
    def post(self, req):
        return JsonResponse({"message": "Testing post with JWT token"})