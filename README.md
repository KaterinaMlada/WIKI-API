# Wikipedia API

1. Clone the repository
  

2. Install dependencies:
  
    pip install -r requirements.txt
   

3. Run migrations:
    
    python manage.py migrate
    

4. Run the server:
   
    python manage.py runserver
 

5. Use the API endpoint:
    

example: 

curl -H "Accept-Language: cs" -w "%{http_code}\n" http://localhost:8000/wiki/abcdefghj/

curl -H "Accept-Language: cs" -w ", %{http_code}\n" http://localhost:8000/wiki/rumbellion

curl -H "Accept-Language: cs" -w ", %{http_code}\n" http://localhost:8000/wiki/rum/

curl -H "Accept-Language: en" -w ", %{http_code}\n" http://localhost:8000/wiki/Pathofexile/

curl -H "Accept-Language: ru" -w ", %{http_code}\n" http://localhost:8000/wiki/rusko/

## Testing

To run tests, use:

python manage.py test


