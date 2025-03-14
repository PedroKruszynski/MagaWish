import httpx
import respx

from maga_wish.modules.products.dtos import GetProductByIdDTO
from maga_wish.shared.environment.main import settings


class GetProductByIdService:
    async def getProductById(self, data: GetProductByIdDTO) -> None:
        url = f"{settings.PRODUCTS_API_URL}/{data.id}"

        with respx.mock:
            mock_data = {
                str(product_id := "550e8400-e29b-41d4-a716-446655440000"): {
                    "id": product_id,
                    "title": "Mock Product A",
                    "price": 10.99,
                    "image": "http://iamAImage_A.com",
                    "brand": "brandA",
                    "reviewScore": 1,
                },
                str(product_id := "123e4567-e89b-12d3-a456-426614174000"): {
                    "id": product_id,
                    "title": "Mock Product B",
                    "price": 20.49,
                    "image": "http://iamAImage_B.com",
                    "brand": "brandB",
                    "reviewScore": 2,
                },
                str(product_id := "767fe8dc-3f6a-4565-bf5f-d334cbec87d3"): {
                    "id": product_id,
                    "title": "Mock Product C",
                    "price": 15.75,
                    "image": "http://iamAImage_C.com",
                    "brand": "brandC",
                    "reviewScore": 3,
                },
                str(product_id := "a4380281-edbb-4fa7-8407-827b5673da90"): {
                    "id": product_id,
                    "title": "Mock Product D",
                    "price": 25.25,
                    "image": "http://iamAImage_D.com",
                    "brand": "brandD",
                    "reviewScore": 4,
                },
                str(product_id := "65bbca14-1c60-4274-9f54-24d47f297965"): {
                    "id": product_id,
                    "title": "Mock Product E",
                    "price": 55.15,
                    "image": "http://iamAImage_E.com",
                    "brand": "brandE",
                    "reviewScore": 5,
                },
            }

            def dynamic_response(request):
                product_id = str(request.url.path.split("/")[-1])
                return httpx.Response(
                    200, json=mock_data.get(product_id, {"error": "Product not found"})
                )

            respx.get(url).mock(side_effect=dynamic_response)

            async with httpx.AsyncClient() as client:
                response = await client.get(url)
            return response.json()
