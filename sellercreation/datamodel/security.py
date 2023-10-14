from werkzeug.security import safe_str_cmp
from sellercreation.datamodel.sellerConfig import SellerValidation

def authenticate(email, phone):
    user = SellerValidation.find_by_username(email,phone)
    if user and safe_str_cmp(email, phone):
        return user
