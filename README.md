# CLTV (CheckLockTimeVerify)
Colección de scripts en Python que permiten bloquear [Chauchas](https://www.chaucha.cl) en la red hasta que se cumpla la condición (nHeight >= nLockTime).

## Modo de uso

### Crear dirección P2SH:

El script [create.py](https://github.com/proyecto-chaucha/CLTV/blob/master/create.py) permite generar un script de desbloqueo y una dirección P2SH (que comienza con la letra M mayúscula) en base a un tiempo máximo de bloqueo **locktime** y una llave privada **privkey**.

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

## Prueba de funcionamiento

P2SH Address: [MSxD8GjPmL6oMKLEVedg3ui8Tq5utXAodx](http://insight.chaucha.cl/address/MSxD8GjPmL6oMKLEVedg3ui8Tq5utXAodx)

## Fuentes

* [BIP 16: Pay to Script Hash](https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki)
* [BIP 65: OP_CHECKLOCKTIMEVERIFY](https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki)
* [Using CLTV in Scripts](https://github.com/ChristopherA/Learning-Bitcoin-from-the-Command-Line/blob/master/09_2_Using_CLTV_in_Scripts.md)
* [CHECKLOCKTIMEVERIFY (BIP65) Demos](https://github.com/petertodd/checklocktimeverify-demos/)
* [Script: Freezing funds until a time in the future](https://en.bitcoin.it/wiki/Script#Freezing_funds_until_a_time_in_the_future)
