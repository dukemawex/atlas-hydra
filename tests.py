import asyncio
from unittest.mock import AsyncMock
from atlas import Atlas
async def main():
 a=Atlas(); a.cypher=AsyncMock(return_value={"rows":[{"canonical":"Sam Ratnaparkhi"}]})
 out=await a.aliases('@sam'); assert out['rows'][0]['canonical']=='Sam Ratnaparkhi'; print('atlas-offline-contracts-ok')
if __name__=='__main__': asyncio.run(main())
