from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "media" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL,
    "file_id" VARCHAR(500) NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "media";"""


MODELS_STATE = (
    "eJztmW9v0zwQwL9KlVdDgmnNlnUPQkht10FhbR9tHc8jEIrcxE2tOnawHUaF+t2xnaT5H1"
    "rE2Cr6at35zrn72b472d8Nn7oQ8+MRdBEwXra+GwT4UP7IDzxvGSAIUrESCDDDkeZGZcYF"
    "A46QwjnAHEqRC7nDUCAQJVJKQoyVkDpSEREvFYUEfQmhLagHxQIyOfDpsxQj4sJvkCf/Bk"
    "t7jiB2c44iV31by22xCrRsSMSVVlRfm9kOxaFPUuVgJRaUbLQREUrqQQIZEFBNL1io3Ffe"
    "xWEmEUWepiqRixkbF85BiEUm3C0ZOJQoftIbrgP01FdemO2zztnF6fnZhVTRnmwknXUUXh"
    "p7ZKgJjKfGWo8DASINjTHlpv+WyPUXgFWjS/QL8KTLRXgJqiZ6iSDFl26Z38TPB99sDIkn"
    "FgrayUkDrQ/dm/7b7s2R1HqmoqFyG0ebexwPmdGYQpoinCMM7ar9V08xY7KfIK2tQFoNIK"
    "0IpDrQ82VmayrBDDjLe8BcuzRCTVqnWx7yTb8oAQR4Go8KUkUQJ7hbZwHdEEN3CviyKgPm"
    "FRozIU9UbSF1+SEn7ltODMAKU1AB793tZFxNL2NSQHhHZHSfXOSI5y2MuPj8NI93AzAVtX"
    "La5/wLzh7io1H3/+L57l9PepoC5cJjehY9Qa+QNDWeHTJmor+v6XKrbNmQLItFh4XEBqJM"
    "8FJSEMiH1RRTqwJHNzY7Tn48TaoNFKfD0eB22h39m9uql93pQI2YWroqSI/OC8Q3k7T+G0"
    "7fttS/rY+T8aC4ozd604+G8gmEgtqE3tvAzYadiBNRbgUDRh3IOazIMz1KMQSkJtVk7QrL"
    "OJOGD7Vyuxau7ZeuN5lc51atN5wWTsLdqDe4OWrr5ZJKSMBsKk+hhhyyyl6sh7za0pcx+n"
    "n9q8AZl7c/mV2iCviPaZ6edsyT0/ML66zTsS5ONqWwPNRUE3vDN4pljnkEt9Sf5VmXQV9R"
    "BpFH3sOVhj2UfgPiVOXuuLO6i6d5cpDXyT5JpKkXDNxv+q3s9pHRyZhgtDv73dt+93JgrB"
    "+npdVcKzrZhHd9A6sCesS2VUiCHgP+zue4YLhPvewfOMlNHa9DQ8ahHYBK5E3VqGB5qEf5"
    "eoS47ctiLU+oPcPUWe5c7asnOGDOY3YYVGH/Qkect3ysrth4NQ+Jo9i2xpTAY9kzvjb+3j"
    "Z5h0uhdA8Url14xUGLZ7h6fwMx0FBru5LSfc/etCfrh2wqupAhZ1HVVsQjjY0FSHUOF2K/"
    "v4l4sAuxr7IfjE/Ltvc1GZP9vLIxLWubpwLLqn8qUGP5OqWOxg4QY/X9BNje6omg3fBE0C"
    "6/tcgvCkgqqnz91WzG5HA1W3c1+6jPMOsfApW+vA=="
)
