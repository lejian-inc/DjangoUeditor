#coding=utf-8
from django.db import connection
import os

class TenantSchemaMixin(object):

    def _append_tenant_schema(self, path):
        """
        判断是否使用了还有TenantMixin的storage，如果是的话，则返回路径
        需要附带上tenant schema目录前缀。这里的
        """
        try:
            from tenant_schemas.storage import TenantStorageMixin
            if issubclass(self.storage.__class__, TenantStorageMixin):
                path = os.path.join("{}".format(connection.tenant.schema_name), path)
        except:
            pass
        return path 


