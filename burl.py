#!/opt/homebrew/bin/python3.11

import click
import requests

# Define User-Agent strings for different browsers
USER_AGENTS = {
    "chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "firefox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "edge": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/91.0.864.48"
}

def make_request(url, headers, verbose):
    response = requests.get(url, headers=headers)
    
    if verbose:
        click.echo(f"Status Code: {response.status_code}")
        click.echo("Response Headers:")
        for key, value in response.headers.items():
            click.echo(f"{key}: {value}")
        click.echo("Response Content:")
        click.echo(response.text)  # Print the first 500 characters of the response content
    else:
        click.echo(response.text)  # Print the first 500 characters of the response content

@click.command()
@click.argument('url')
@click.option('-h', '--header', multiple=True, help="Headers to include in the request")
@click.option('-v', '--verbose', is_flag=True, help="Verbose output")
@click.option('-b', '--browser', type=click.Choice(USER_AGENTS.keys()), default='chrome', help="Browser to mimic (default: chrome)")
def main(url, header, verbose, browser):
    """Mimic a real browser using cURL-like arguments in Python"""
    
    # Default headers to mimic a real browser
    headers = {
        "User-Agent": USER_AGENTS[browser],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    # Add additional headers from command-line arguments
    for h in header:
        key, value = h.split(":", 1)
        headers[key.strip()] = value.strip()

    make_request(url, headers, verbose)

if __name__ == "__main__":
    main()
