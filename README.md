# Wikipedia API

1. Clone the repository
  

2. Install dependencies:
  
    pip install -r requirements.txt

3. Run the server:
   
    python manage.py runserver
 

4. Use the API endpoint:
    

example: 

curl -H "Accept-Language: cs" -w "%{http_code}\n" http://localhost:8000/wiki/abcdefghj/

curl -H "Accept-Language: cs" -w ", %{http_code}\n" http://localhost:8000/wiki/rumbellion

curl -H "Accept-Language: cs" -w ", %{http_code}\n" http://localhost:8000/wiki/rum/

curl -H "Accept-Language: cs" -w ", %{http_code}\n" http://localhost:8000/wiki/Path_of_Exile/


When you click on the link, it will take you to a page that will display the wanted information in Czech language.

## Testing

To run tests, use:

python manage.py test





