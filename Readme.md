# GraphQL wrapper for a RESTful API

## Usage
### Install dependencies and start the server
```
# Install Dependencies
make install

# Create .env file and add api keys to it
https://developer.marvel.com/account

PUBLIC_KEY=abcd
PRIVATE_KEY=efgh

# Run the server
make run
```

### Go to the /graphql url
http://localhost:5000/graphql

### Sample Query
```json
{  
  comics {       
      id,
    	title,
    	characters {
    	  available
    	  returned
    	  collectionURI,
        items {
          resourceURI
        },
        details {
          results {
            name
          }
        }
    	}
  }
}
```
