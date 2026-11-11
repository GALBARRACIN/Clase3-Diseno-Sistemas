"""ViajaYa: código de referencia (mini sistema) para los fragmentos de completar."""
from abc import ABC, abstractmethod
import threading
import copy
from dataclasses import dataclass

# ---------- Singleton ----------
class ConexionReservas:
    _instance = None
    _lock = threading.Lock()
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._inicializada = False
        return cls._instance
    def __init__(self):
        if not self._inicializada:
            print("Conectando al sistema de reservas")
            self._inicializada = True
    @classmethod
    def obtener(cls):
        return cls()

# ---------- Factory Method ----------
class Pasaje(ABC):
    def __init__(self, origen, destino, precio):
        if precio < 0: raise ValueError("precio negativo")
        self._origen, self._destino, self._precio = origen, destino, precio
    @property
    def precio(self): return self._precio
    @abstractmethod
    def mostrar_info(self): ...
class PasajeAvion(Pasaje):
    def __init__(self, o, d, p, aerolinea): super().__init__(o, d, p); self._aerolinea = aerolinea
    def mostrar_info(self): print(f"AVION {self._origen}-{self._destino} {self._aerolinea}: {self._precio}")
class PasajeMicro(Pasaje):
    def mostrar_info(self): print(f"MICRO {self._origen}-{self._destino}: {self._precio}")
class PasajeTren(Pasaje):
    def mostrar_info(self): print(f"TREN {self._origen}-{self._destino}: {self._precio}")

class CreadorPasaje(ABC):
    @abstractmethod
    def crear_pasaje(self, origen, destino, precio): ...
    def registrar_pasaje(self, origen, destino, precio):
        p = self.crear_pasaje(origen, destino, precio)
        p.mostrar_info()
        return p
class CreadorAvion(CreadorPasaje):
    def __init__(self, aerolinea): self._aerolinea = aerolinea
    def crear_pasaje(self, o, d, p): return PasajeAvion(o, d, p, self._aerolinea)
class CreadorMicro(CreadorPasaje):
    def crear_pasaje(self, o, d, p): return PasajeMicro(o, d, p)
class CreadorTren(CreadorPasaje):
    def crear_pasaje(self, o, d, p): return PasajeTren(o, d, p)

# ---------- Builder ----------
class Reserva:
    def __init__(self): self.pasajes=[]; self.tasa=0; self.equipaje=0; self.seguro=0
    def subtotal(self): return sum(p.precio for p in self.pasajes)
    def calcular_total(self): return self.subtotal()+self.tasa+self.equipaje+self.seguro
class ReservaBuilder:
    def __init__(self): self.reiniciar()
    def reiniciar(self): self._r = Reserva()
    def set_pasajes(self, ps): self._r.pasajes = list(ps)
    def set_tasa(self): self._r.tasa = 10
    def set_equipaje(self): self._r.equipaje = 30
    def set_seguro(self): self._r.seguro = self._r.subtotal()*0.03
    def build(self):
        r = self._r; self.reiniciar(); return r
class DirectorReserva:
    def __init__(self, builder): self._b = builder
    def set_builder(self, b): self._b = b
    def construir_simple(self, ps):
        self._b.set_pasajes(ps); self._b.set_tasa(); return self._b.build()
    def construir_completa(self, ps):
        self._b.set_pasajes(ps); self._b.set_tasa(); self._b.set_equipaje(); self._b.set_seguro()
        return self._b.build()

# ---------- Decorator ----------
class Componente(ABC):
    @property
    @abstractmethod
    def precio(self): ...
    @property
    @abstractmethod
    def descripcion(self): ...
class PasajeBase(Componente):
    def __init__(self, nombre, precio): self._n, self._p = nombre, precio
    @property
    def precio(self): return self._p
    @property
    def descripcion(self): return self._n
class Extra(Componente):
    def __init__(self, c): self._c = c
class Equipaje(Extra):
    @property
    def precio(self): return self._c.precio + 30
    @property
    def descripcion(self): return self._c.descripcion + " + equipaje"
class SeguroViaje(Extra):
    @property
    def precio(self): return self._c.precio * 1.02
    @property
    def descripcion(self): return self._c.descripcion + " + seguro"
class Comida(Extra):
    @property
    def precio(self): return self._c.precio + 12
    @property
    def descripcion(self): return self._c.descripcion + " + comida"

# ---------- Adapter ----------
class PasarelaLegada:
    def pay(self, centavos, token): return f"OK:{centavos}"
class PasarelaPago(ABC):
    @abstractmethod
    def cobrar(self, monto): ...
class AdaptadorLegada(PasarelaPago):
    def __init__(self): self._legada = PasarelaLegada()
    def cobrar(self, monto):
        return self._legada.pay(int(round(monto*100)), "tk").startswith("OK")

# ---------- Observer ----------
class Observador(ABC):
    @abstractmethod
    def actualizar(self, mensaje): ...
class AlertaPrecio:
    def __init__(self, vuelo): self._vuelo=vuelo; self._suscriptores=[]
    def suscribir(self, o):
        if o not in self._suscriptores: self._suscriptores.append(o)
    def nuevo_precio(self, texto):
        for o in self._suscriptores: o.actualizar(texto)
class Viajero(Observador):
    def __init__(self, n): self.n=n; self.llamadas=0
    def actualizar(self, mensaje): self.llamadas+=1; print(f"{self.n} recibe: {mensaje}")

# ---------- Strategy ----------
class Vuelo:
    def __init__(self, nombre, precio, minutos, escalas, puntaje=0):
        self.nombre, self.precio, self.minutos, self.escalas, self.puntaje = nombre, precio, minutos, escalas, puntaje
class EstrategiaOrden(ABC):
    @abstractmethod
    def ordenar(self, vuelos): ...
class PorPrecio(EstrategiaOrden):
    def ordenar(self, v): return sorted(v, key=lambda x: x.precio)
class PorDuracion(EstrategiaOrden):
    def ordenar(self, v): return sorted(v, key=lambda x: x.minutos)
class PorRecomendados(EstrategiaOrden):
    def ordenar(self, v): return sorted(v, key=lambda x: x.puntaje, reverse=True)
class Buscador:
    def __init__(self, vuelos): self._v=vuelos; self._e=None
    def set_criterio(self, e): self._e = e
    def resultados(self): return self._e.ordenar(self._v)

# ---------- Chain of Responsibility ----------
class Validador(ABC):
    def __init__(self): self._sig=None; self.llamadas=0
    def set_siguiente(self, v): self._sig=v; return v
    def validar(self, datos):
        self.llamadas+=1
        if not self._revisar(datos): return False
        return self._sig.validar(datos) if self._sig else True
    @abstractmethod
    def _revisar(self, datos): ...
class ValidadorDocumento(Validador):
    def _revisar(self, d): return bool(d.get("documento"))
class ValidadorDisponibilidad(Validador):
    def _revisar(self, d): return d.get("asientos", 0) > 0
class ValidadorPago(Validador):
    def _revisar(self, d): return d.get("metodo") in ("tarjeta", "transferencia")

# ================= Los otros 15 patrones =================

# ---------- Abstract Factory ----------
class FabricaMercado(ABC):
    @abstractmethod
    def crear_moneda(self): ...
    @abstractmethod
    def crear_documento(self): ...
class FabricaArgentina(FabricaMercado):
    def crear_moneda(self): return "ARS"
    def crear_documento(self): return "DNI"
class FabricaEuropa(FabricaMercado):
    def crear_moneda(self): return "EUR"
    def crear_documento(self): return "Pasaporte"
def formulario(fabrica): return f"{fabrica.crear_documento()} en {fabrica.crear_moneda()}"

# ---------- Prototype ----------
class PaqueteBase:
    def __init__(self, nombre, componentes): self.nombre=nombre; self.componentes=componentes
    def clonar(self): return copy.deepcopy(self)

# ---------- Bridge ----------
class Canal(ABC):
    @abstractmethod
    def enviar(self, texto): ...
class Mail(Canal):
    def enviar(self, texto): return f"MAIL: {texto}"
class SMS(Canal):
    def enviar(self, texto): return f"SMS: {texto}"
class Confirmacion(ABC):
    def __init__(self, canal): self._canal = canal
class ConfirmacionVuelo(Confirmacion):
    def enviar(self): return self._canal.enviar("Vuelo confirmado")
class ConfirmacionHotel(Confirmacion):
    def enviar(self): return self._canal.enviar("Hotel confirmado")

# ---------- Composite / Visitor ----------
class ItemViaje(ABC):
    @property
    @abstractmethod
    def precio(self): ...
class ItemVuelo(ItemViaje):
    def __init__(self, p): self._p = p
    @property
    def precio(self): return self._p
    def aceptar(self, v): return v.visitar_vuelo(self)
class ItemHotel(ItemViaje):
    def __init__(self, p): self._p = p
    @property
    def precio(self): return self._p
    def aceptar(self, v): return v.visitar_hotel(self)
class PaqueteTuristico(ItemViaje):
    def __init__(self, hijos): self._hijos = hijos
    @property
    def precio(self): return sum(h.precio for h in self._hijos)
class VisitorCosto:
    def __init__(self): self.total = 0
    def visitar_vuelo(self, v): self.total += v.precio
    def visitar_hotel(self, h): self.total += h.precio

# ---------- Facade ----------
class ReservaFacade:
    def __init__(self): self.log = []
    def reservar(self, ruta, monto):
        self.log.append("disponibilidad"); self.log.append("cobro")
        self.log.append("voucher"); self.log.append("mail")
        return f"VOUCHER-{ruta}"

# ---------- Flyweight ----------
class Icono:
    def __init__(self, tipo): self.tipo = tipo
class FabricaIconos:
    def __init__(self): self._cache = {}
    def obtener(self, tipo):
        if tipo not in self._cache:
            self._cache[tipo] = Icono(tipo)
        return self._cache[tipo]

# ---------- Proxy ----------
class ServicioPrecios:
    def __init__(self): self.llamadas = 0
    def consultar(self, o, d): self.llamadas += 1; return 100.0
class ProxyPrecios:
    def __init__(self, real): self._real = real; self._cache = {}
    def consultar(self, o, d):
        clave = (o, d)
        if clave in self._cache: return self._cache[clave]
        self._cache[clave] = self._real.consultar(o, d)
        return self._cache[clave]

# ---------- Command ----------
class Comando(ABC):
    @abstractmethod
    def ejecutar(self): ...
    @abstractmethod
    def deshacer(self): ...
class AgregarItem(Comando):
    def __init__(self, itinerario, item): self._i, self._item = itinerario, item
    def ejecutar(self): self._i.append(self._item)
    def deshacer(self): self._i.remove(self._item)

# ---------- Interpreter ----------
class Expresion(ABC):
    @abstractmethod
    def evaluar(self, ctx): ...
class TemporadaBaja(Expresion):
    def evaluar(self, ctx): return ctx["temporada"] == "baja"
class Destino(Expresion):
    def __init__(self, d): self._d = d
    def evaluar(self, ctx): return ctx["destino"] == self._d
class Y(Expresion):
    def __init__(self, a, b): self._a, self._b = a, b
    def evaluar(self, ctx): return self._a.evaluar(ctx) and self._b.evaluar(ctx)
class O(Expresion):
    def __init__(self, a, b): self._a, self._b = a, b
    def evaluar(self, ctx): return self._a.evaluar(ctx) or self._b.evaluar(ctx)

# ---------- Iterator ----------
class Resultados:
    def __init__(self, paginas): self._paginas = paginas
    def __iter__(self):
        for pagina in self._paginas:
            for r in pagina:
                yield r

# ---------- Mediator ----------
class Filtro:
    def __init__(self, med, valor): self._med = med; self.valor = valor
    def set(self, valor):
        self.valor = valor
        self._med.notificar(self, valor)
class MediadorFiltros:
    def __init__(self):
        self.directos = Filtro(self, False)
        self.escalas = Filtro(self, 2)
    def notificar(self, origen, valor):
        if origen is self.directos and valor:
            self.escalas.valor = 0

# ---------- Memento ----------
@dataclass(frozen=True)
class MementoPago:
    paso: int
class FormularioPago:
    def __init__(self): self.paso = 1
    def avanzar(self): self.paso += 1
    def guardar(self): return MementoPago(self.paso)
    def restaurar(self, m): self.paso = m.paso

# ---------- State ----------
class EstadoReserva(ABC):
    def confirmar(self, r): return False
    def cancelar(self, r): return False
class Pendiente(EstadoReserva):
    def confirmar(self, r): r.estado = Confirmada(); return True
    def cancelar(self, r): r.estado = Cancelada(); return True
class Confirmada(EstadoReserva):
    def cancelar(self, r): r.estado = Cancelada(); return True
class Cancelada(EstadoReserva): pass
class ReservaEstado:
    def __init__(self): self.estado = Pendiente()
    def confirmar(self): return self.estado.confirmar(self)
    def cancelar(self): return self.estado.cancelar(self)

# ---------- Template Method ----------
class Voucher(ABC):
    def emitir(self):
        return ["validar", "cobrar", "generar:" + self.generar(), "enviar"]
    @abstractmethod
    def generar(self): ...
class VoucherMicro(Voucher):
    def generar(self): return "MICRO"