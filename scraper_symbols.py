from requests import get

url = 'https://query1.finance.yahoo.com/v1/finance/search?q={query}&lang=en-US&region=US&quotesCount=6&newsCount=2&listsCount=2&enableFuzzyQuery=false&quotesQueryId=tss_match_phrase_query&multiQuoteQueryId=multi_quote_single_token_query&newsQueryId=news_cie_vespa&enableCb=true&enableNavLinks=true&enableEnhancedTrivialQuery=true&enableResearchReports=true&enableCulturalAssets=true&enableLogoUrl=true&researchReportsCount=2'

headers = {
  'authority': 'query1.finance.yahoo.com',
  'accept': '*/*',
  'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
  'cookie': 'A1=d=AQABBB883mUCEA89HnwX6H3SqGALG6hxyBkFEgEBAQGN32XoZR6exyMA_eMAAA&S=AQAAAs9wJ1u_aGuCL6m-03VthZI; A3=d=AQABBB883mUCEA89HnwX6H3SqGALG6hxyBkFEgEBAQGN32XoZR6exyMA_eMAAA&S=AQAAAs9wJ1u_aGuCL6m-03VthZI; A1S=d=AQABBB883mUCEA89HnwX6H3SqGALG6hxyBkFEgEBAQGN32XoZR6exyMA_eMAAA&S=AQAAAs9wJ1u_aGuCL6m-03VthZI; cmp=t=1709072934&j=0&u=1---; gpp=DBAA; gpp_sid=-1; axids=gam=y-TIoqrc1E2uLuTv31EVX2HMZpweNo1q3q~A&dv360=eS1kTUdlOVJwRTJ1SG1OeE1Cc0duV3hmZ2hDaUEzNjhLb35B&ydsp=y-EUffdVhE2uLYp.daRS.ZVIWMTy.OFwCF~A&tbla=y-qEOp3WpE2uL7ch37UCkTPUBxLsf9FWHj~A; PRF=t%3DMGLU3.SA%252B%255EBVSP%26newChartbetateaser%3D0%252C1710282544216',
  'dnt': '1',
  'origin': 'https://finance.yahoo.com',
  'referer': 'https://finance.yahoo.com/quote/MGLU3.SA?.tsrc=fin-srch',
  'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
  'sec-ch-ua-mobile': '?1',
  'sec-ch-ua-platform': '"Android"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'sec-gpc': '1',
  'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36 Edg/122.0.0.0'
}

symbols = []

# loop de a até z
for i in range(97, 123):
    char = chr(i)
    response = get(url.format(query=char), headers=headers)
    
    if not response.ok:
        print(f'Erro ao buscar a letra {char}')
        continue

    dados = response.json()
    quotes = dados.get('quotes')

    if quotes is None:
        print(f'Nenhuma informação para a letra {char}')
        continue
    
    
    for quote in quotes:
        try:
            symbols.append(quote['symbol'])
            print(quote)
        except:
            #print(quote)
            break

print(symbols)


