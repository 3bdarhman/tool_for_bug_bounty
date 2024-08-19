import asyncio
import aiohttp
import sys

async def check_status(session, subdomain):
    url = f'http://{subdomain}'
    try:
        async with session.get(url, timeout=3) as response:
            if response.status == 200:
                return (subdomain, response.status)
            else:
                return (subdomain, None)
    except asyncio.TimeoutError:
        return (subdomain, None)
    except aiohttp.ClientError:
        return (subdomain, None)

async def start(file_path, output_file):
    async with aiohttp.ClientSession() as session:
        tasks = []
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    subdomain = line.strip()
                    if subdomain:
                        task = check_status(session, subdomain)
                        tasks.append(task)
            results = await asyncio.gather(*tasks)

            with open(output_file, 'w') as out_file:
                for subdomain, status in results:
                    if status == 200:
                        output_line = f"{subdomain} => status = {status}\n"
                        out_file.write(output_line)
                        print(output_line.strip())  
        except FileNotFoundError:
            print(f'File not found: {file_path}')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 status_for_sub.py <subdomain_file> <output_file>')
        sys.exit(0)
    
    subdomainFile = sys.argv[1]
    outputFile = sys.argv[2]
    asyncio.run(start(subdomainFile, outputFile))
