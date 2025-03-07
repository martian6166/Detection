
from pymongo import MongoClient

import bcrypt

def hash_password(password):
    """
    Hash a password using bcrypt.
    
    Args:
        password (str): The plain text password to hash
        
    Returns:
        bytes: The hashed password
    """
    # Convert string to bytes and generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(password, hashed_password):
    """
    Check if a provided password matches the hashed password.
    
    Args:
        password (str): The plain text password to check
        hashed_password (bytes): The previously hashed password
        
    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        # Check if the password matches the hash
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    except Exception:
        # Return False if there's any error (e.g., invalid hash)
        return False



def create_user(db_uri: str, db_name: str, collection_name: str, document: dict) -> str:
    """
    Inserts a new document into the specified MongoDB collection.

    Parameters:
        db_uri (str): MongoDB connection URI.
        db_name (str): Name of the database.
        collection_name (str): Name of the collection.
        document (dict): The document to insert.

    Returns:
        str: The ID of the inserted document.
    """
    # Connect to MongoDB
    client = MongoClient(db_uri)
    db = client[db_name]
    collection = db[collection_name]
    # Insert the document
    s = collection.find_one({"username":document.get('username')})
    password = hash_password(document.get('password'))
    document['password']= password
    if s==None:
        result = collection.insert_one(document)

        return str(result.inserted_id)
    else:
        client.close()
        return False
    
    # Close the connection
    

def login_user(db_uri: str, db_name: str, collection_name: str, document: dict) :
    """
    Inserts a new document into the specified MongoDB collection.

    Parameters:
        db_uri (str): MongoDB connection URI.
        db_name (str): Name of the database.
        collection_name (str): Name of the collection.
        document (dict): The document to insert.

    Returns:
        str: The ID of the inserted document.
    """
    # Connect to MongoDB
    client = MongoClient(db_uri)
    db = client[db_name]
    collection = db[collection_name]
    
    # Insert the document
    s = collection.find_one({"username":document["username"]})
    print(s)
    print(document.get('username'))
    if s==None:
        return {False,True}
    else:

        if check_password(password=document['password'],hashed_password=s['password']):

            return {str(s['_id']),s['username']}
        else:
            return {False,True}
    # Close the connection
    