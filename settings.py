from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


# Throttling constants. The API can be called up to MAX_LEN times in SECONDS seconds
MAX_LEN = 5
SECONDS = 30

# Token constants
SECRET_KEY = "42bb1604cbbd11e94a0c3bc18e452592ab5ed4fe53da5e72b380dbc7b9c515b0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Alphavantage apikey
AV_APIKEY = "X86NOH6II01P7R24"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
