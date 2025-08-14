import sys

from passlib.context import CryptContext

key = sys.argv[1]
pwd_context = CryptContext(schemes=["des_crypt"], deprecated="auto")
print("Input: ", key)
print("Hashed Key: ", pwd_context.hash(key))
