import os
import time
import requests
from bs4 import BeautifulSoup
import re

sent_links = set()

def get_product_url(href):
    if href and href.startswith('/'):
        return f"https://www.amazon.in{href.split('?')[0]}"
    return href.split('?')[0] if href else ''

def fetch_amazon_loot_deals():
    amazon_urls = [
        "https://www.amazon.in/electronics/b/?ie=UTF8&node=976419031&ref_=nav_cs_electronics",
        "https://www.amazon.in/computers-accessories/b/?ie=UTF8&node=976392031",
        "https://www.amazon.in/mobiles-accessories/b/?ie=UTF8&node=1389401031",
        "https://www.amazon.in/home-kitchen/b/?ie=UTF8&node=976442031",
        "https://www.amazon.in/sports-fitness-outdoors/b/?ie=UTF8&node=3403642031",
        "https://www.amazon.in/clothing-accessories/b/?ie=UTF8&node=1571271031",
        "https://www.amazon.in/beauty/b/?ie=UTF8&node=1355016031",
        "https://www.amazon.in/books/b/?ie=UTF8&node=976389031",
        "https://www.amazon.in/toys-games/b/?ie=UTF8&node=1350380031",
        "https://www.amazon.in/automotive/b/?ie=UTF8&node=4772060031",
        "https://www.amazon.in/deals/b/?ie=UTF8&node=3419926031",
        "https://www.amazon.in/gp/goldbox",
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    all_loot_deals = []
    
    for url_index, url in enumerate(amazon_urls):
        print(f"\n🔍 Searching Amazon category {url_index + 1}/{len(amazon_urls)} for LOOT DEALS...")
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch Amazon page. Status code: {response.status_code}")
                continue
            
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.select("[data-component-type='s-search-result']") or soup.select(".s-result-item") or soup.select("[data-asin]")
            print(f"  Found {len(items)} items on the page.")
            
            for i, item in enumerate(items):
                # --- DEBUG PRINT: Attempting to find product info ---
                print(f"  Processing Amazon item {i+1}/{len(items)}...")
                
                title_elem = (item.select_one("h2 a span") or 
                              item.select_one("h2 span") or 
                              item.select_one(".a-size-medium") or
                              item.select_one(".a-size-base-plus") or
                              item.select_one(".a-truncate-cut"))

                link_elem = item.select_one("h2 a") or item.select_one("a")
                price_elem = (item.select_one(".a-price-whole") or 
                              item.select_one(".a-price .a-offscreen"))
                mrp_elem = (item.select_one(".a-text-price .a-offscreen") or 
                            item.select_one(".a-price.a-text-price .a-offscreen"))

                if not (title_elem and link_elem and price_elem and mrp_elem):
                    # --- DEBUG PRINT: Information missing ---
                    print(f"    - SKIPPING: Missing title ({bool(title_elem)}), link ({bool(link_elem)}), price ({bool(price_elem)}), or MRP ({bool(mrp_elem)}).")
                    continue

                try:
                    price_text = re.sub(r'[₹,]', '', price_elem.text.strip())
                    price_value = float(price_text)
                    
                    mrp_text = re.sub(r'[₹,]', '', mrp_elem.text.strip())
                    mrp_value = float(mrp_text)
                    
                    # --- DEBUG PRINT: Found all info, checking for discount ---
                    print(f"    - Found: '{title_elem.text.strip()[:40]}...' | Price: ₹{price_value} | MRP: ₹{mrp_value}")

                    if mrp_value > price_value:
                        discount = round(100 - ((price_value / mrp_value) * 100), 1)
                        if discount >= 90:
                            full_link = get_product_url(link_elem.get('href', ''))
                            if full_link not in sent_links:
                                loot_deal = {
                                    "source": "Amazon",
                                    "title": title_elem.text.strip(),
                                    "price": price_value,
                                    "mrp": mrp_value,
                                    "discount": discount,
                                    "link": full_link
                                }
                                all_loot_deals.append(loot_deal)
                                sent_links.add(full_link)
                                print(f"🚨 LOOT DEAL FOUND! {discount}% OFF: {title_elem.text.strip()[:50]}...")
                except (ValueError, AttributeError) as e:
                    print(f"    - SKIPPING: Error converting price/MRP to float: {e}")
                    continue
            
            print(f"✅ Amazon category scan complete.")
        
        except Exception as e:
            print(f"❌ Error scanning Amazon category: {e}")
            continue
    
    return all_loot_deals
    
def fetch_flipkart_loot_deals():
    flipkart_urls = [
        "https://www.flipkart.com/mobiles/pr?sid=tyy,4io",
        "https://www.flipkart.com/laptops/pr?sid=6bo,b5g",
        "https://www.flipkart.com/televisions/pr?sid=ckf,czl",
        "https://www.flipkart.com/cameras/pr?sid=ahh,fgn",
        "https://www.flipkart.com/home-kitchen/pr?sid=j9e",
        "https://www.flipkart.com/clothing-accessories/pr?sid=reh",
        "https://www.flipkart.com/toys/pr?sid=p65",
        "https://www.flipkart.com/books/pr?sid=bks",
        "https://www.flipkart.com/auto-accessories/pr?sid=6z1",
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    all_loot_deals = []
    
    for url_index, url in enumerate(flipkart_urls):
        print(f"\n🔍 Searching Flipkart category {url_index + 1}/{len(flipkart_urls)} for LOOT DEALS...")
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch Flipkart page. Status code: {response.status_code}")
                continue
            
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.find_all("div", class_="_1AtVbE")
            print(f"  Found {len(items)} items on the page.")
            
            for i, item in enumerate(items):
                # --- DEBUG PRINT: Attempting to find product info ---
                print(f"  Processing Flipkart item {i+1}/{len(items)}...")
                
                title_elem = item.find("div", class_="_4rR01T") or item.find("a", class_="s1Q9rs")
                link_elem = item.find("a", class_="_1fQZEK") or item.find("a", class_="s1Q9rs")
                price_elem = item.find("div", class_="_30jeq3")
                mrp_elem = item.find("div", class_="_3I9_wc")

                if not (title_elem and link_elem and price_elem and mrp_elem):
                    # --- DEBUG PRINT: Information missing ---
                    print(f"    - SKIPPING: Missing title ({bool(title_elem)}), link ({bool(link_elem)}), price ({bool(price_elem)}), or MRP ({bool(mrp_elem)}).")
                    continue

                try:
                    price_text = re.sub(r'[₹,]', '', price_elem.text.strip())
                    price_value = float(price_text)
                    
                    mrp_text = re.sub(r'[₹,]', '', mrp_elem.text.strip())
                    mrp_value = float(mrp_text)

                    # --- DEBUG PRINT: Found all info, checking for discount ---
                    print(f"    - Found: '{title_elem.text.strip()[:40]}...' | Price: ₹{price_value} | MRP: ₹{mrp_value}")

                    if mrp_value > price_value:
                        discount = round(100 - ((price_value / mrp_value) * 100), 1)
                        if discount >= 90:
                            full_link = f"https://www.flipkart.com{link_elem.get('href')}"
                            if full_link not in sent_links:
                                loot_deal = {
                                    "source": "Flipkart",
                                    "title": title_elem.text.strip(),
                                    "price": price_value,
                                    "mrp": mrp_value,
                                    "discount": discount,
                                    "link": full_link
                                }
                                all_loot_deals.append(loot_deal)
                                sent_links.add(full_link)
                                print(f"🚨 LOOT DEAL FOUND! {discount}% OFF: {title_elem.text.strip()[:50]}...")
                except (ValueError, AttributeError) as e:
                    print(f"    - SKIPPING: Error converting price/MRP to float: {e}")
                    continue
            
            print(f"✅ Flipkart category scan complete.")
        
        except Exception as e:
            print(f"❌ Error scanning Flipkart category: {e}")
            continue
    
    return all_loot_deals

def write_loot_deals_to_file(loot_deals):
    if not loot_deals:
        print("❌ No LOOT DEALS found")
        return
    
    print(f"💾 Writing {len(loot_deals)} LOOT DEALS to file...")
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    header = f"\n{'='*60}\n🚨 LOOT DEALS ALERT - {timestamp} 🚨\n{'='*60}\n\n"
    
    try:
        with open("loot_deals.txt", "a", encoding="utf-8") as file:
            file.write(header)
            
            for deal in loot_deals:
                message = (
                    f"🎯 LOOT DEAL: {deal['title']}\n"
                    f"🛒 Source: {deal['source']}\n"
                    f"💰 Current Price: ₹{deal['price']:,.0f}\n"
                    f"💸 Original MRP: ₹{deal['mrp']:,.0f}\n"
                    f"🔥 MASSIVE DISCOUNT: {deal['discount']}% OFF!\n"
                    f"💸 You Save: ₹{deal['mrp'] - deal['price']:,.0f}\n"
                    f"🔗 GRAB NOW: {deal['link']}\n"
                    f"⚡ Hurry! This might be a pricing error!\n"
                    f"{'-'*60}\n"
                )
                file.write(message)
            
            print(f"\n✅ All {len(loot_deals)} loot deals saved to 'loot_deals.txt'")
    except Exception as e:
        print(f"❌ Error writing loot deals file: {e}")

# Main execution - LOOT DEAL HUNTER
if __name__ == "__main__":
    print("🎯 LOOT DEAL HUNTER ACTIVATED!")
    print("🚀 Searching for deals with 70%+ discounts...")
    print("⚡ These could be pricing errors or great sales!")
    
    scan_count = 0
    
    while True:
        try:
            scan_count += 1
            print(f"\n--- LOOT SCAN #{scan_count} - {time.strftime('%H:%M:%S')} ---")
            
            all_deals = []
            
            # Scrape from Amazon
            amazon_deals = fetch_amazon_loot_deals()
            all_deals.extend(amazon_deals)
            
            # Scrape from Flipkart
            flipkart_deals = fetch_flipkart_loot_deals()
            all_deals.extend(flipkart_deals)
            
            if all_deals:
                print(f"\n🎉 JACKPOT! Found a total of {len(all_deals)} LOOT DEALS!")
                for deal in all_deals:
                    savings = deal['mrp'] - deal['price']
                    print(f"💎 {deal['title'][:60]}... ({deal['source']})")
                    print(f"   💰 ₹{deal['price']:,.0f} (was ₹{deal['mrp']:,.0f}) - SAVE ₹{savings:,.0f}!")
                    print(f"   🔥 {deal['discount']}% OFF!")
                
                write_loot_deals_to_file(all_deals)
                
            else:
                print("❌ No LOOT DEALS found this scan")
                print("💡 Loot deals are rare - keep scanning!")
                
        except KeyboardInterrupt:
            print(f"\n👋 LOOT HUNTER stopped after {scan_count} scans")
            break
        except Exception as e:
            print(f"❌ Error during loot scan: {e}")
        
        print(f"\n💤 Waiting 30 seconds before next LOOT SCAN...")
        print("⏰ Loot deals disappear fast - frequent scanning recommended!")
        time.sleep(30)