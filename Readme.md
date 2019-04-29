# GraphQL wrapper for a RESTful API

## Usage
### Install dependencies and start the server
```
# Install Dependencies
make install

# Run the server
make run
```

### Go to the /graphql url
http://localhost:5000/graphql

### Sample Query
```json
{  
  comics(comicId:"123456") {    
    character {      
          id        
    }  
  }
}
```
