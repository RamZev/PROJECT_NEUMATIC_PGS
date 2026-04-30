from django.contrib import admin

from .models.caja_models import Caja, CajaDetalle, CajaArqueo, CajaMedioPago
from .models.compra_models import Compra, DetalleCompra
from .models.factura_models import Factura, DetalleFactura, SerialFactura
from .models.recibo_models import DetalleRecibo, RetencionRecibo, DepositoRecibo, TarjetaRecibo, ChequeRecibo
from .models.venta_models import StockCliente

admin.site.register(Caja)
admin.site.register(CajaDetalle)
admin.site.register(CajaArqueo)
admin.site.register(CajaMedioPago)
admin.site.register(Compra)
admin.site.register(DetalleCompra)
admin.site.register(Factura)
admin.site.register(DetalleFactura)
admin.site.register(SerialFactura)
admin.site.register(DetalleRecibo)
admin.site.register(RetencionRecibo)
admin.site.register(DepositoRecibo)
admin.site.register(TarjetaRecibo)
admin.site.register(ChequeRecibo)
admin.site.register(StockCliente)