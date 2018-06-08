# CLTV (CheckLockTimeVerify)
Colección de scripts en Python que permiten bloquear [Chauchas](https://www.chaucha.cl) en la red hasta que el número de bloque sea mayor al parametro locktime definido.

## Modo de uso

### Crear dirección P2SH:

El script [create.py](https://github.com/proyecto-chaucha/CLTV/blob/master/create.py) permite generar un "script de desbloqueo" y una dirección P2SH (que comienza con la letra M mayúscula) en base a un tiempo máximo de bloqueo **locktime** y una llave privada **privkey**.

*(Es recomendado definir el parámetro locktime en "bloques" y no en formato EPOCH)*

```
$> python3 create.py <locktime> <privkey>
> P2SH ADDRESS: <address que inicia con M>
> REDEEM SCRIPT: <script de desbloqueo>
```

Esta dirección P2SH es capaz de aceptar Chauchas que solo podrán ser gastadas con la utilización del script de desbloqueo.

### Gastar Chauchas almacenadas en la dirección P2SH:

```
$> python3 spend.py <locktime> <privkey> <address receptora>
> BALANCE (<dirección P2SH>): <cantidad de Chauchas>
> RESPONSE: {"txid":"<ID de transacción>"}
```

El script [spend.py](https://github.com/proyecto-chaucha/CLTV/blob/master/spend.py) permite contruir una transacción que incluye todos los fondos almacenados en la dirección P2SH, que es generada por el parametro **locktime** y la llave privada **privkey**, los cuales serán enviados a la dirección receptora **address** a través de la Red Chaucha.

## Ejemplo

1. Se utilizó el archivo [create.py](https://github.com/proyecto-chaucha/CLTV/blob/master/create.py) para generar un script de desbloqueo, usando la llave privada *5KjD85fz6RgN7XNGUPWzBaUyV8Fha2tbdfgi3hjwhrjzRCuAjPb* y el bloque *327000* como parámetros de entrada.

```
$> python3 create.py 327000 5KjD85fz6RgN7XNGUPWzBaUyV8Fha2tbdfgi3hjwhrjzRCuAjPb
> P2SH ADDRESS: MJQu639U3WKH6pQdkX4FasFta1GKLFZ11X
> REDEEM SCRIPT: 0358fd04b1752102e683f8f0b0e6ca5c9edec7e85cde47338ace009dde18ebee0e19a1621522c247ac
```

2. Se enviaron 20 CHA a la dirección P2SH generada, que puedes observar en el [explorador de bloques](http://insight.chaucha.cl/tx/b0c946e3252bf45079ac2334effac59bc064df546ce7dfb5b86433508979664b).

3. **ESPERANDO LA GENERACIÓN DEL BLOQUE #327.000**

## Prueba de funcionamiento

P2SH Address: [MSxD8GjPmL6oMKLEVedg3ui8Tq5utXAodx](http://insight.chaucha.cl/address/MSxD8GjPmL6oMKLEVedg3ui8Tq5utXAodx)

## Fuentes

* [BIP 16: Pay to Script Hash](https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki)
* [BIP 65: OP_CHECKLOCKTIMEVERIFY](https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki)
* [Using CLTV in Scripts](https://github.com/ChristopherA/Learning-Bitcoin-from-the-Command-Line/blob/master/09_2_Using_CLTV_in_Scripts.md)
* [CHECKLOCKTIMEVERIFY (BIP65) Demos](https://github.com/petertodd/checklocktimeverify-demos/)
* [Script: Freezing funds until a time in the future](https://en.bitcoin.it/wiki/Script#Freezing_funds_until_a_time_in_the_future)
