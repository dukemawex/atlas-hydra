import asyncio
from atlas import Atlas
async def main():
 a=Atlas(); await a.ingest_fixture(); print('ALIAS',await a.aliases('@sam')); print('CONFLICT-AWARE PROJECT',await a.resolve('Phoenix')); print('MISSING',await a.missing('Who owns Project Apollo?'))
if __name__=='__main__': asyncio.run(main())
