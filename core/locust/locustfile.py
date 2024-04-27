from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    
    def on_start(self):
        response = self.client.post("/accounts/api/v1/jwt/create/",data={
            "email": "admin@admin.com",
            "password": "1234567a"
            }).jason()
        self.client.headers = {"Authorization": f'Bearer {response.get("access",None)}'}
   
        
    
    @task
    def post_list(self):
        self.client.get("/blog/api/v1/posts/")
        
    @task
    def category_list(self):
        self.client.get("/blog/api/v1/category/")
        