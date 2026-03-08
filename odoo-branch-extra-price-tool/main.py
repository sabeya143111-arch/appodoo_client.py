import xmlrpc.client

class OdooClient:
    def __init__(self, url, db, username, password):
        self.url = url.rstrip("/")
        self.db = db
        self.username = username
        self.password = password
        self.uid = None
        self.models = None

    def connect(self):
        common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        uid = common.authenticate(self.db, self.username, self.password, {})
        if not uid:
            raise Exception("Authentication failed. Check DB / username / password.")
        self.uid = uid
        self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")
        return uid

    def get_branches(self, branch_model="x.branch"):
        branch_ids = self.models.execute_kw(
            self.db, self.uid, self.password,
            branch_model, 'search',
            [[]]
        )
        branches = self.models.execute_kw(
            self.db, self.uid, self.password,
            branch_model, 'read',
            [branch_ids, ['name']]
        )
        return branches

    def find_products_by_codes(self, model_codes, product_model="product.product"):
        domain = [('default_code', 'in', model_codes)]
        product_ids = self.models.execute_kw(
            self.db, self.uid, self.password,
            product_model, 'search',
            [domain]
        )
        return product_ids

    def read_products(self, product_ids, fields, product_model="product.product"):
        return self.models.execute_kw(
            self.db, self.uid, self.password,
            product_model, 'read',
            [product_ids, fields]
        )

    def write_product(self, product_id, values, product_model="product.product"):
        return self.models.execute_kw(
            self.db, self.uid, self.password,
            product_model, 'write',
            [[product_id], values]
        )
