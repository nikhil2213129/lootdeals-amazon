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
        "https://www.amazon.in/prime?ref_=nav_cs_primelink_nonmember",
        "https://www.amazon.in/s/?_encoding=UTF8&bbn=81107433031&rh=n%3A81107433031%2Cp_85%3A10440599031&pd_rd_w=HrZc4&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/Lifelong-Dumbbells-Equipment-Exercise-Warranty/dp/B09W5PSTBP/?_encoding=UTF8&pd_rd_w=6ziYw&content-id=amzn1.sym.211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_p=211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_crs_zg_bs_1984443031",
        "https://www.amazon.in/gp/css/homepage.html?ref_=footer_ya",
        "https://www.amazon.in/SANSI-MAYO-Womens-Snake-Steel/dp/B0DJ7GHJSX/?_encoding=UTF8&pd_rd_w=WeZZh&content-id=amzn1.sym.6ca15ca4-a8c2-4aba-b219-9c4cb936bb3c&pf_rd_p=6ca15ca4-a8c2-4aba-b219-9c4cb936bb3c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/fresh?ref_=nav_cs_grocery",
        "https://www.amazon.in/gp/help/customer/display.html?nodeId=200507590&ref_=nav_cs_help",
        "https://www.amazon.in/KITOOL-Crinkle-Slicing-Stainless-Vegetable/dp/B0923XG5DW/?_encoding=UTF8&pd_rd_w=s3S0K&content-id=amzn1.sym.81f4df47-d71a-46ce-b8de-32884f91242b&pf_rd_p=81f4df47-d71a-46ce-b8de-32884f91242b&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/b/?_encoding=UTF8&ie=UTF8&node=5257496031&pd_rd_w=qs3S8&content-id=amzn1.sym.9ff36f11-82d6-4600-a8fb-e52bb32e171c&pf_rd_p=9ff36f11-82d6-4600-a8fb-e52bb32e171c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/Sports/b/?ie=UTF8&node=1984443031&ref_=nav_cs_sports",
        "https://www.amazon.in/s/?_encoding=UTF8&bbn=1388921031&rh=n%3A1388921031%2Cp_89%3AboAt&pd_rd_w=trRrJ&content-id=amzn1.sym.71850b5e-5657-45e6-935e-feb77b5645a2&pf_rd_p=71850b5e-5657-45e6-935e-feb77b5645a2&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/video-games/b/?ie=UTF8&node=976460031&ref_=nav_cs_video_games",
        "https://www.amazon.in/earthsave-Lunch-Bag-Eco-Friendly-Drawstring/dp/B093K12NYZ/?_encoding=UTF8&pd_rd_w=M9gdX&content-id=amzn1.sym.32378808-0263-4069-9a58-814866f75c85&pf_rd_p=32378808-0263-4069-9a58-814866f75c85&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/Allen-Solly-Regular-AMKP317G04249_Jet-Black_Large/dp/B06Y2FG6R7/?_encoding=UTF8&pd_rd_w=O5SOC&content-id=amzn1.sym.211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_p=211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_crs_zg_bs_1571271031",
        "https://www.amazon.in/Vaux-29T-Single-Speed-Adult/dp/B095799XH1/?_encoding=UTF8&pd_rd_w=Qcztg&content-id=amzn1.sym.10fbb0e8-f7f0-4de9-bee0-d6ae0d1b703e&pf_rd_p=10fbb0e8-f7f0-4de9-bee0-d6ae0d1b703e&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/Puma-Womens-Smashic-White-Peony-Matte-Sneaker/dp/B0BSLJBMB8/?_encoding=UTF8&pd_rd_w=9A0RW&content-id=amzn1.sym.de84ee3f-a07f-47cd-ac44-50f5d6cbb587&pf_rd_p=de84ee3f-a07f-47cd-ac44-50f5d6cbb587&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_a2i_gw_cml",
        "https://www.amazon.in/b/?_encoding=UTF8&node=100293361031&pd_rd_w=ZEb4R&content-id=amzn1.sym.0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_p=0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_NSS",
        "https://www.amazon.in/gp/bestsellers/?ref_=nav_cs_bestsellers",
        "https://www.amazon.in/SMAART-CRAAFTS-Shakti-Solid-Bedside/dp/B0CCSFVPYW/?_encoding=UTF8&pd_rd_w=v2LdJ&content-id=amzn1.sym.152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_p=152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/HARLEY-DAVIDSON-Motorcycle-440cc-booking-Ex-Showroom/dp/B0FDGY2KM1/?_encoding=UTF8&pd_rd_w=TIgqP&content-id=amzn1.sym.c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_p=c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en4_",
        "https://www.amazon.in/Wopno-Furniture-Sheesham-Wooden-Rosewood/dp/B0DRLDW1YY/?_encoding=UTF8&pd_rd_w=v2LdJ&content-id=amzn1.sym.152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_p=152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/s/?_encoding=UTF8&i=fashion&bbn=90505325031&rh=n%3A6648217031%2Cn%3A90418239031%2Cn%3A90505325031%2Cn%3A7459780031%2Cn%3A1953602031%2Cn%3A1968253031%2Cn%3A1968255031%2Cp_85%3A10440599031&hidden-keywords=-sponsored&pd_rd_w=uoDz3&content-id=amzn1.sym.1350f669-3050-4d58-9819-7ff3e03b8408&pf_rd_p=1350f669-3050-4d58-9819-7ff3e03b8408&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_unk",
        "https://www.amazon.in/gp/help/customer/display.html?nodeId=200545940&ref_=footer_cou",
        "https://www.amazon.in/b/?_encoding=UTF8&ie=UTF8&node=1388921031&pd_rd_w=CzJp8&content-id=amzn1.sym.82b20790-8877-4d70-8f73-9d8246e460aa&pf_rd_p=82b20790-8877-4d70-8f73-9d8246e460aa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/#skippedLink",
        "https://www.amazon.in/s/?_encoding=UTF8&bbn=1380374031&rh=n%3A1380374031%2Cp_n_format_browse-bin%3A19560799031&pd_rd_w=lou1G&content-id=amzn1.sym.4d494d65-8009-406a-9a50-5e08a16212d7&pf_rd_p=4d494d65-8009-406a-9a50-5e08a16212d7&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/b/?node=6637738031&ref_=nav_cs_amazonbasics",
        "https://www.amazon.in/gp/help/customer/display.html?nodeId=202075050&ref_=footer_iba",
        "https://www.amazon.in/Large-Dish-Drying-Mat-Microfiber/dp/B0DMW81DMW/?_encoding=UTF8&pd_rd_w=2le9c&content-id=amzn1.sym.60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_p=60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/DDN_R_-Stainless-Organiser-Transparent-Container/dp/B0FCBFNFVT/?_encoding=UTF8&pd_rd_w=8fN1r&content-id=amzn1.sym.a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_p=a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/gp/help/customer/display.html?nodeId=200507590&ref_=footer_gw_m_b_he",
        "https://www.amazon.in/Plantex-Self-Adhesive-Multipurpose-Bathroom-Accessories/dp/B0B3J7Q14R/?_encoding=UTF8&pd_rd_w=8fN1r&content-id=amzn1.sym.a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_p=a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/minitv?ref_=nav_avod_desktop_topnav",
        "https://www.amazon.in/gp/browse.html?node=6967393031&ref_=footer_mobapp",
        "https://www.amazon.in/TEX-RO-Storage-Box-Organisers-Multi-Purpose/dp/B0DSKK7CZX/?_encoding=UTF8&pd_rd_w=8fN1r&content-id=amzn1.sym.a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_p=a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/Nervfit-Launched-Smartwatch-Bluetooth-Waterproof/dp/B0DY6BP9GQ/?_encoding=UTF8&pd_rd_w=B4QHc&content-id=amzn1.sym.a8cbddb8-9da6-400b-b864-eb4b2042931c&pf_rd_p=a8cbddb8-9da6-400b-b864-eb4b2042931c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/gp/css/returns/homepage.html?ref_=footer_hy_f_4",
        "https://www.amazon.in/gp/redirect.html/ref=footer_fb?location=http://www.facebook.com/AmazonIN&token=2075D5EAC7BB214089728E2183FD391706D41E94&6",
        "https://www.amazon.in/gp/sva/dashboard?ref_=nav_cs_apay",
        "https://www.amazon.in/PowerA-Controller-Black-Officially-Licensed/dp/B08F4444HM/?_encoding=UTF8&pd_rd_w=XL4v0&content-id=amzn1.sym.6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_p=6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/gp/redirect.html?location=https://www.instagram.com/amazondotin&token=264882C912E9D005CB1D9B61F12E125D5DF9BFC7&source=standards",
        "https://accelerator.amazon.in/?ref_=map_1_b2b_GW_FT",
        "https://www.amazon.in/stores/page/preview/ref=man_sbc_LA_HALO1_BAU_NOV23_3/ref=man_sbc_LA_HALO1_BAU_NOV23_3/ref=man_sbc_LA_HALO1_BAU_NOV23_3/ref=man_sbc_hetvclp_2_1/?_encoding=UTF8&_encoding=UTF8&_encoding=UTF8&_encoding=UTF8&_encoding=UTF8&_encoding=UTF8&_encoding=UTF8&isPreview=1&isSlp=1&asins=B0B8YTGC23%2CB0D25MMHH2%2CB0DY7FPFLH%2CB09F6S8BT6%2CB0DBLLYXVV%2CB0DHL6N6BG%2CB0D4LJ9WVW%2CB0CZ6QH357%2CB0DDCDTPVC%2CB0DVGBNVM2%2CB0D9BYGT8J%2CB0D9BX9DMB%2CB0CZ6PVG32%2CB07MNNH484%2CB0DZHNQJQW%2CB0DPSD1PG5%2CB0CD1S96SM%2CB0DKNM4GPM%2CB0DZHMX6D3%2CB0DR2Q2R44%2CB0CZ6TRNGT%2CB0C4DPCKDJ%2CB0DCZH5MPC&pd_rd_w=B35GV&content-id=amzn1.sym.46d2074e-6340-47f1-8d20-54821e9d3161&pf_rd_p=46d2074e-6340-47f1-8d20-54821e9d3161&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/Qshare-Travel-Soap-Box-Transparent/dp/B0DHVT9Y3J/?_encoding=UTF8&pd_rd_w=2le9c&content-id=amzn1.sym.60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_p=60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/Erios-Storage-Countertop-Organiser-Bathroom/dp/B0F8QR17ZX/?_encoding=UTF8&pd_rd_w=8fN1r&content-id=amzn1.sym.a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_p=a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/TRIUMPH-Scrambler-Metallic-Booking-Ex-Showroom/dp/B0F53D4PR8/?_encoding=UTF8&pd_rd_w=TIgqP&content-id=amzn1.sym.c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_p=c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en4_",
        "https://www.amazon.in/health-and-personal-care/b/?ie=UTF8&node=1350384031&ref_=nav_cs_hpc",
        "https://www.amazon.in/OPTIFINE-Wooden-Multipurpose-Adjustable-Bedroom/dp/B0F7G6ZR9V/?_encoding=UTF8&pd_rd_w=ZEb4R&content-id=amzn1.sym.0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_p=0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_NSS",
        "https://www.amazon.in/DIVIJA-STORE-Multipurpose-Breakfast-Ergonomic/dp/B0DK78YK54/?_encoding=UTF8&pd_rd_w=ZEb4R&content-id=amzn1.sym.0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_p=0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_NSS",
        "https://www.amazon.in/WOODIOGRAPHY-Ceiling-Decoration-Home-Corded-Electric/dp/B0BHTQZ16T/?_encoding=UTF8&pd_rd_w=3Rle5&content-id=amzn1.sym.91b7b9d8-d2b8-4319-9dd3-9b1005242396&pf_rd_p=91b7b9d8-d2b8-4319-9dd3-9b1005242396&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.science",
        "https://www.amazon.in/Books/b/?ie=UTF8&node=976389031&ref_=nav_cs_books",
        "https://www.amazon.in/Nervfit-AMOLED-Calling-Waterproof-Monitor/dp/B0D6KYB414/?_encoding=UTF8&pd_rd_w=B4QHc&content-id=amzn1.sym.a8cbddb8-9da6-400b-b864-eb4b2042931c&pf_rd_p=a8cbddb8-9da6-400b-b864-eb4b2042931c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/gift-card-store/b/?ie=UTF8&node=3704982031&ref_=nav_cs_gc",
        "https://www.amazon.in/Amazon-Brand-Symbol-Polo_SS19PLS2_Fog-Teal_Large/dp/B07MZG27XK/?_encoding=UTF8&pd_rd_w=O5SOC&content-id=amzn1.sym.211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_p=211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_crs_zg_bs_1571271031",
        "https://www.amazon.in/b/?_encoding=UTF8&ie=UTF8&node=5257472031&pd_rd_w=qs3S8&content-id=amzn1.sym.9ff36f11-82d6-4600-a8fb-e52bb32e171c&pf_rd_p=9ff36f11-82d6-4600-a8fb-e52bb32e171c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/gp/help/customer/display.html?nodeId=201083470&ref_=footer_swc",
        "https://www.amazon.in/b/?_encoding=UTF8&node=10894223031&pd_rd_w=2le9c&content-id=amzn1.sym.60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_p=60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/VIDA-Electric-Removable-Batteries-Ex-Showroom/dp/B0DPL35R9D/?_encoding=UTF8&pd_rd_w=TIgqP&content-id=amzn1.sym.c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_p=c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en4_",
        "https://www.amazon.in/s/?_encoding=UTF8&bbn=1380442031&rh=n%3A1380442031%2Cp_n_format_browse-bin%3A19560802031&pd_rd_w=lou1G&content-id=amzn1.sym.4d494d65-8009-406a-9a50-5e08a16212d7&pf_rd_p=4d494d65-8009-406a-9a50-5e08a16212d7&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/Ebee-Layer-Storage-Organizer-Wheels/dp/B07SCR4Q6P/?_encoding=UTF8&pd_rd_w=8fN1r&content-id=amzn1.sym.a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_p=a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/PALAK-Plastic-Multipurpose-Kitchen-Organizer/dp/B0CV3GFVKP/?_encoding=UTF8&pd_rd_w=ZEb4R&content-id=amzn1.sym.0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_p=0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_NSS",
        "https://www.amazon.in/s/?_encoding=UTF8&bbn=84514752031&rh=n%3A84514752031%2Cp_85%3A10440599031&pd_rd_w=HrZc4&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/FOMQUAZLI-Coffee-Straws-Tumbler-Smoothie/dp/B0D4J17DQF/?_encoding=UTF8&pd_rd_w=s3S0K&content-id=amzn1.sym.81f4df47-d71a-46ce-b8de-32884f91242b&pf_rd_p=81f4df47-d71a-46ce-b8de-32884f91242b&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/s/?_encoding=UTF8&bbn=81107432031&rh=n%3A81107432031%2Cp_85%3A10440599031&pd_rd_w=HrZc4&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/TRONICA-Firefly-Bluetooth-Theater-PenDrive/dp/B0CK78VY4J/?_encoding=UTF8&pd_rd_w=Sb5ou&content-id=amzn1.sym.049f4884-e005-4b6b-9e95-2b599decd624&pf_rd_p=049f4884-e005-4b6b-9e95-2b599decd624&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/Hero-Sprint-Shimano-Front-Suspension-Multi-Speed/dp/B0BRPV1VX1/?_encoding=UTF8&pd_rd_w=Qcztg&content-id=amzn1.sym.10fbb0e8-f7f0-4de9-bee0-d6ae0d1b703e&pf_rd_p=10fbb0e8-f7f0-4de9-bee0-d6ae0d1b703e&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/MAYNOS-Suction-Phone-Midnight-Mystery%EF%BC%88Black%EF%BC%89/dp/B0CKXJ67ZB/?_encoding=UTF8&pd_rd_w=2le9c&content-id=amzn1.sym.60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_p=60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/KTM-Duke-Booking-Ex-Showroom-Price/dp/B0F836FH3J/?_encoding=UTF8&pd_rd_w=TIgqP&content-id=amzn1.sym.c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_p=c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en4_",
        "https://www.amazon.in/Toys-Games/b/?ie=UTF8&node=1350380031&ref_=nav_cs_toys",
        "https://www.amazon.in/business?ref=footer_aingw",
        "https://www.amazon.in/Amazon-Custom/b/?ie=UTF8&node=32615889031&ref_=nav_cs_custom",
        "https://supply.amazon.com/?ref_=footer_sta&lang=en-IN",
        "https://www.amazon.in/London-Hills-Cotton-Oversized-T-Shirts/dp/B0C8YKXJ5G/?_encoding=UTF8&pd_rd_w=9A0RW&content-id=amzn1.sym.de84ee3f-a07f-47cd-ac44-50f5d6cbb587&pf_rd_p=de84ee3f-a07f-47cd-ac44-50f5d6cbb587&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_a2i_gw_cml",
        "https://www.amazon.in/s/?_encoding=UTF8&i=fashion&bbn=90505325031&rh=n%3A6648217031%2Cn%3A90418239031%2Cn%3A90505325031%2Cn%3A7459780031%2Cn%3A1953602031%2Cn%3A1968253031%2Cn%3A1968256031%2Cp_85%3A10440599031&hidden-keywords=-sponsored&pd_rd_w=uoDz3&content-id=amzn1.sym.1350f669-3050-4d58-9819-7ff3e03b8408&pf_rd_p=1350f669-3050-4d58-9819-7ff3e03b8408&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_unk",
        "https://www.amazon.in/TRIUMPH-Phantom-Black-Booking-Ex-Showroom/dp/B0F535N7JT/?_encoding=UTF8&pd_rd_w=TIgqP&content-id=amzn1.sym.c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_p=c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en4_",
        "https://www.amazon.in/s/?_encoding=UTF8&i=home-improvement&rh=n%3A60834830031%2Cp_36%3A-39900%2Cp_72%3A1318476031&dc=&fs=true&qid=1714744556&rnid=1318475031&ref=sr_nr_p_72_1&ds=v1%3AObcyf9vB3S72PU7NAfGZ%2FbllKjFxF%2BIh8NlJQg5c1A8%22&pd_rd_w=plRzf&content-id=amzn1.sym.0a250fc6-18a4-49da-8c15-ae7cde5579f2&pf_rd_p=0a250fc6-18a4-49da-8c15-ae7cde5579f2&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/b/?_encoding=UTF8&node=28253258031&ref=ls_gwc_mb_en8_&pd_rd_w=TIgqP&content-id=amzn1.sym.c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_p=c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en4_",
        "https://www.amazon.in/gp/history",
        "https://www.amazon.in/auto-deliveries/landing?ref_=nav_cs_sns",
        "https://www.amazon.in/gp/help/customer/display.html?nodeId=200534380&ref_=footer_privacy",
        "https://www.amazon.in/OBAGE-Essential-4-Theatre-Digital-Control/dp/B0D8BB16XK/?_encoding=UTF8&pd_rd_w=Sb5ou&content-id=amzn1.sym.049f4884-e005-4b6b-9e95-2b599decd624&pf_rd_p=049f4884-e005-4b6b-9e95-2b599decd624&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/b/ref=surl_fashion/?_encoding=UTF8&node=6648217031&pd_rd_w=Olk6F&content-id=amzn1.sym.2e7b6e14-61a5-4727-ab58-89719b5e191b&pf_rd_p=2e7b6e14-61a5-4727-ab58-89719b5e191b&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=k0REW&pd_rd_r=1d7ed20f-8863-44f9-a9bf-11a354339cdc&ref_=pd_hp_d_hero_unk",
        "https://www.amazon.in/s/?_encoding=UTF8&k=noise&i=electronics&rh=n%3A1388921031%2Cp_n_condition-type%3A8609960031%2Cp_36%3A-200000&pd_rd_w=CzJp8&content-id=amzn1.sym.82b20790-8877-4d70-8f73-9d8246e460aa&pf_rd_p=82b20790-8877-4d70-8f73-9d8246e460aa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/b/?_encoding=UTF8&ie=UTF8&node=84514749031&pd_rd_w=uoDz3&content-id=amzn1.sym.1350f669-3050-4d58-9819-7ff3e03b8408&pf_rd_p=1350f669-3050-4d58-9819-7ff3e03b8408&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_unk",
        "https://www.amazon.in/WEZOSHINET-Premium-Tumbler-Leather-Beverages/dp/B0CJ361H9M/?_encoding=UTF8&pd_rd_w=2le9c&content-id=amzn1.sym.60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_p=60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://brandservices.amazon.in/?ref=AOINABRLGNRFOOT&ld=AOINABRLGNRFOOT",
        "https://www.amazon.in/GoSriKi-Anarkali-Printed-Dupatta-Yellow-GS_XL_Yellow_X-Large/dp/B0DD78S3M2/?_encoding=UTF8&pd_rd_w=O5SOC&content-id=amzn1.sym.211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_p=211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_crs_zg_bs_1571271031",
        "https://www.amazon.in/Safari-Laptop-Backpack-Raincover-college/dp/B097JJ2CK6/?_encoding=UTF8&pd_rd_w=VC7CT&content-id=amzn1.sym.211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_p=211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_crs_zg_bs_976392031",
        "https://www.amazon.in/THELA-GAADI-Cotton-Funky-Socks/dp/B0BBMC7PFL/?_encoding=UTF8&pd_rd_w=WeZZh&content-id=amzn1.sym.6ca15ca4-a8c2-4aba-b219-9c4cb936bb3c&pf_rd_p=6ca15ca4-a8c2-4aba-b219-9c4cb936bb3c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/flights?ref_=nav_cs_apay_desktop_topnav_flights",
        "https://www.amazon.in/s/?_encoding=UTF8&i=electronics&bbn=1388921031&rh=n%3A1388921031%2Cp_89%3ABoult&pd_rd_w=trRrJ&content-id=amzn1.sym.71850b5e-5657-45e6-935e-feb77b5645a2&pf_rd_p=71850b5e-5657-45e6-935e-feb77b5645a2&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/b/?_encoding=UTF8&node=1380374031&pd_rd_w=U9f7C&content-id=amzn1.sym.f8e82c51-0408-4554-a158-9be4d776850d&pf_rd_p=f8e82c51-0408-4554-a158-9be4d776850d&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/Sony-CFI-ZCT1W-DualSense-wireless-controller/dp/B08GZ6QNTC/?_encoding=UTF8&pd_rd_w=XL4v0&content-id=amzn1.sym.6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_p=6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/EvoFox-Programmable-Ultra-Responsive-Sensitive-Software/dp/B0CLS6F44T/?_encoding=UTF8&pd_rd_w=XL4v0&content-id=amzn1.sym.6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_p=6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/Nervfit-Waterproof-Bluetooth-Performance-Smartwatch/dp/B0D6KYB415/?_encoding=UTF8&pd_rd_w=B4QHc&content-id=amzn1.sym.a8cbddb8-9da6-400b-b864-eb4b2042931c&pf_rd_p=a8cbddb8-9da6-400b-b864-eb4b2042931c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/Lifelong-Adjustable-Weight-50-Manufacturers-LLKS03/dp/B0C862R9VF/?_encoding=UTF8&pd_rd_w=6ziYw&content-id=amzn1.sym.211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_p=211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_crs_zg_bs_1984443031",
        "https://www.amazon.in/s/?_encoding=UTF8&i=fashion&bbn=90505325031&rh=n%3A6648217031%2Cn%3A90418239031%2Cn%3A90505325031%2Cn%3A7459780031%2Cn%3A1953602031%2Cn%3A11400137031%2Cn%3A15330093031%2Cp_85%3A10440599031&s=apparel&hidden-keywords=-sponsored&pd_rd_w=uoDz3&content-id=amzn1.sym.1350f669-3050-4d58-9819-7ff3e03b8408&pf_rd_p=1350f669-3050-4d58-9819-7ff3e03b8408&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_unk",
        "https://www.amazon.in/stores/page/preview/ref=man_sbc_LA_HALO1_BAU_NOV23_3/ref=man_sbc_LA_HALO1_BAU_NOV23_3/ref=man_sbc_LA_HALO1_BAU_NOV23_3/ref=man_sbc_hetvclp_2_3/?_encoding=UTF8&_encoding=UTF8&_encoding=UTF8&_encoding=UTF8&_encoding=UTF8&_encoding=UTF8&_encoding=UTF8&isPreview=1&isSlp=1&asins=B0DBRL1SYQ%2CB0D3DZ1SPM%2CB0BFFHGML2%2CB0C82ZHYQ8%2CB0CX5DW4WT%2CB0CX5FTKSH%2CB0DHL66ZB8%2CB0DCZMPRXC%2CB0D9P2MNMS%2CB0CZLLPXRJ%2CB0DC6SMTL7%2CB0D9BWTQLL%2CB0F391JVWF%2CB0D9C1ZTC1%2CB0D3X9275X%2CB0D7QBSYD3%2CB0DRV6WTZY&pd_rd_w=B35GV&content-id=amzn1.sym.46d2074e-6340-47f1-8d20-54821e9d3161&pf_rd_p=46d2074e-6340-47f1-8d20-54821e9d3161&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/CONSA-Organic-Buckthorn-Berry-Powder/dp/B0DV3D41GY/?_encoding=UTF8&pd_rd_w=ZEb4R&content-id=amzn1.sym.0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_p=0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_NSS",
        "https://www.amazon.in/EDEUEQUE-Engineered-Tabletop-Gold-Coating/dp/B0BV318374/?_encoding=UTF8&pd_rd_w=v2LdJ&content-id=amzn1.sym.152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_p=152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/mobile-phones/b/?ie=UTF8&node=1389401031&ref_=nav_cs_mobiles",
        "https://www.amazon.in/",
        "https://www.amazon.in/b/?_encoding=UTF8&ie=UTF8&node=1388921031&pd_rd_w=trRrJ&content-id=amzn1.sym.71850b5e-5657-45e6-935e-feb77b5645a2&pf_rd_p=71850b5e-5657-45e6-935e-feb77b5645a2&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/s/?_encoding=UTF8&i=home-improvement&rh=n%3A95174669031%2Cp_36%3A3444810031%2Cp_72%3A1318476031&pd_rd_w=plRzf&content-id=amzn1.sym.0a250fc6-18a4-49da-8c15-ae7cde5579f2&pf_rd_p=0a250fc6-18a4-49da-8c15-ae7cde5579f2&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/Well-Set-Multipurpose-Chipser-Unbreakable/dp/B0CG4DY65G/?_encoding=UTF8&pd_rd_w=M9gdX&content-id=amzn1.sym.32378808-0263-4069-9a58-814866f75c85&pf_rd_p=32378808-0263-4069-9a58-814866f75c85&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/CHAIR-DECOR-Velvet-Modern-Armchair/dp/B0FBX1R3GF/?_encoding=UTF8&pd_rd_w=v2LdJ&content-id=amzn1.sym.152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_p=152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/ARQIVO-Crinkle-Stainless-Chopping-Vegetables/dp/B0B8TDXD35/?_encoding=UTF8&pd_rd_w=2le9c&content-id=amzn1.sym.60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_p=60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.shopbop.com/",
        "https://www.amazon.in/Hercules-Streetcat-Pro-IC-Years/dp/B09DL9H1T5/?_encoding=UTF8&pd_rd_w=Qcztg&content-id=amzn1.sym.10fbb0e8-f7f0-4de9-bee0-d6ae0d1b703e&pf_rd_p=10fbb0e8-f7f0-4de9-bee0-d6ae0d1b703e&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/b/?_encoding=UTF8&node=12414705031&pd_rd_w=U9f7C&content-id=amzn1.sym.f8e82c51-0408-4554-a158-9be4d776850d&pf_rd_p=f8e82c51-0408-4554-a158-9be4d776850d&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/XYXX-Solid-Regular-XY_CR14_Polo-Tshirt_1_Blue/dp/B0CBBB5843/?_encoding=UTF8&pd_rd_w=9A0RW&content-id=amzn1.sym.de84ee3f-a07f-47cd-ac44-50f5d6cbb587&pf_rd_p=de84ee3f-a07f-47cd-ac44-50f5d6cbb587&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_a2i_gw_cml",
        "https://www.amazon.in/Amazon-Brand-Symactive-Dumbbells-Workout/dp/B0CV84LYG4/?_encoding=UTF8&pd_rd_w=6ziYw&content-id=amzn1.sym.211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_p=211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_crs_zg_bs_1984443031",
        "https://amazon.jobs",
        "https://www.amazon.in/SMAART-CRAAFTS-Bedside-Carving-Nightstand/dp/B0CR4BCSBC/?_encoding=UTF8&pd_rd_w=v2LdJ&content-id=amzn1.sym.152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_p=152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/Home-Improvement/b/?ie=UTF8&node=4286640031&ref_=nav_cs_hi",
        "https://www.amazon.in/computers-and-accessories/b/?ie=UTF8&node=976392031&ref_=nav_cs_pc",
        "https://www.amazon.in/Light4Life-5-Light-Chandelier-Resturent-Included/dp/B0CVQWH55M/?_encoding=UTF8&pd_rd_w=3Rle5&content-id=amzn1.sym.91b7b9d8-d2b8-4319-9dd3-9b1005242396&pf_rd_p=91b7b9d8-d2b8-4319-9dd3-9b1005242396&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/customer-preferences/edit?ie=UTF8&preferencesReturnUrl=%2F&ref_=topnav_lang",
        "https://www.amazon.in/gp/css/order-history?ref_=nav_orders_first",
        "https://www.amazon.in/Pet-Supplies/b/?ie=UTF8&node=2454181031&ref_=nav_cs_pets",
        "https://www.amazon.in/b/?_encoding=UTF8&node=1380442031&pd_rd_w=U9f7C&content-id=amzn1.sym.f8e82c51-0408-4554-a158-9be4d776850d&pf_rd_p=f8e82c51-0408-4554-a158-9be4d776850d&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://affiliate-program.amazon.in/?utm_campaign=assocshowcase&utm_medium=footer&utm_source=GW&ref_=footer_assoc",
        "https://aws.amazon.com/what-is-cloud-computing/?sc_channel=EL&sc_campaign=IN_amazonfooter",
        "https://www.amazon.in/Baby/b/?ie=UTF8&node=1571274031&ref_=nav_cs_baby",
        "https://www.amazon.in/s/?_encoding=UTF8&node=50916365031&pd_rd_w=9A0RW&content-id=amzn1.sym.de84ee3f-a07f-47cd-ac44-50f5d6cbb587&pf_rd_p=de84ee3f-a07f-47cd-ac44-50f5d6cbb587&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_a2i_gw_cml",
        "https://www.amazon.in/Julienne-Vegetable-Multi-Functional-Adjustable-Stainless/dp/B0F9WQMJV3/?_encoding=UTF8&pd_rd_w=ZEb4R&content-id=amzn1.sym.0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_p=0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_NSS",
        "https://www.amazon.in/ZOBRIX-Compatible-Protection-Frameless-Magsafe/dp/B0DRSPK79Y/?_encoding=UTF8&pd_rd_w=B4QHc&content-id=amzn1.sym.a8cbddb8-9da6-400b-b864-eb4b2042931c&pf_rd_p=a8cbddb8-9da6-400b-b864-eb4b2042931c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/b/?_encoding=UTF8&ie=UTF8&node=5258045031&pd_rd_w=qs3S8&content-id=amzn1.sym.9ff36f11-82d6-4600-a8fb-e52bb32e171c&pf_rd_p=9ff36f11-82d6-4600-a8fb-e52bb32e171c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/CHAIR-DECOR-Upholstered-Armchair-Comfortable/dp/B0FBGGZXLQ/?_encoding=UTF8&pd_rd_w=v2LdJ&content-id=amzn1.sym.152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_p=152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/l/207302681031/?_encoding=UTF8&pd_rd_w=B35GV&content-id=amzn1.sym.46d2074e-6340-47f1-8d20-54821e9d3161&pf_rd_p=46d2074e-6340-47f1-8d20-54821e9d3161&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/AFAST-Attractive-Dazzling-Metal-Glass/dp/B0F9PPVB4S/?_encoding=UTF8&pd_rd_w=3Rle5&content-id=amzn1.sym.91b7b9d8-d2b8-4319-9dd3-9b1005242396&pf_rd_p=91b7b9d8-d2b8-4319-9dd3-9b1005242396&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/gp/cart/view.html?ref_=nav_cart",
        "https://www.amazon.in/b/32702023031?node=32702023031&ld=AZINSOANavDesktop_T3&ref_=nav_cs_sell_T3",
        "https://www.amazon.in/s/?_encoding=UTF8&bbn=1380510031&rh=n%3A1380510031%2Cp_n_format_browse-bin%3A19560790031&pd_rd_w=lou1G&content-id=amzn1.sym.4d494d65-8009-406a-9a50-5e08a16212d7&pf_rd_p=4d494d65-8009-406a-9a50-5e08a16212d7&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/s/?_encoding=UTF8&bbn=1388921031&rh=n%3A1388921031%2Cp_89%3AboAt&pd_rd_w=CzJp8&content-id=amzn1.sym.82b20790-8877-4d70-8f73-9d8246e460aa&pf_rd_p=82b20790-8877-4d70-8f73-9d8246e460aa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/b/?_encoding=UTF8&node=1380510031&pd_rd_w=U9f7C&content-id=amzn1.sym.f8e82c51-0408-4554-a158-9be4d776850d&pf_rd_p=f8e82c51-0408-4554-a158-9be4d776850d&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/KTM-Enduro-Motercycle-Booking-Ex-Showroom/dp/B0F8382VTT/?_encoding=UTF8&pd_rd_w=TIgqP&content-id=amzn1.sym.c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_p=c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en4_",
        "https://www.amazon.in/SMAART-CRAAFTS-Solid-Centre-Table/dp/B0C947RSTB/?_encoding=UTF8&pd_rd_w=v2LdJ&content-id=amzn1.sym.152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_p=152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/gp/new-releases/?ref_=nav_cs_newreleases",
        "https://www.amazon.in/music/prime?ref=footer_apm",
        "https://www.amazon.in/BROVENCE-Foldable-Wardrobe-Organizer-Stackable/dp/B0FJY72BT9/?_encoding=UTF8&pd_rd_w=8fN1r&content-id=amzn1.sym.a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_p=a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/beauty/b/?ie=UTF8&node=1355016031&ref_=nav_cs_beauty",
        "https://www.amazon.in/s/?_encoding=UTF8&i=home-improvement&bbn=61028133031&rh=n%3A61028133031%2Cp_72%3A1318476031%2Cp_36%3A-19900&_encoding=UTF8&qid=1714749719&rnid=3444809031&ref=sr_nr_p_36_3&pd_rd_w=plRzf&content-id=amzn1.sym.0a250fc6-18a4-49da-8c15-ae7cde5579f2&pf_rd_p=0a250fc6-18a4-49da-8c15-ae7cde5579f2&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/s/?_encoding=UTF8&k=zebronics&i=electronics&rh=n%3A976419031%2Cn%3A29561348031%2Cp_89%3AZEBRONICS&pd_rd_w=CzJp8&content-id=amzn1.sym.82b20790-8877-4d70-8f73-9d8246e460aa&pf_rd_p=82b20790-8877-4d70-8f73-9d8246e460aa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/Himajal-Smart-Alkaline-Purifier-White/dp/B09GYK591B/?_encoding=UTF8&pd_rd_w=M9gdX&content-id=amzn1.sym.32378808-0263-4069-9a58-814866f75c85&pf_rd_p=32378808-0263-4069-9a58-814866f75c85&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/l/207302672031/?_encoding=UTF8&pd_rd_w=B35GV&content-id=amzn1.sym.46d2074e-6340-47f1-8d20-54821e9d3161&pf_rd_p=46d2074e-6340-47f1-8d20-54821e9d3161&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/Boldfit-Adjustable-Strengthener-Exercise-Equipment/dp/B0B77X44MX/?_encoding=UTF8&pd_rd_w=6ziYw&content-id=amzn1.sym.211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_p=211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_crs_zg_bs_1984443031",
        "https://www.amazon.in/Timus-Starlite-Hard-Sided-Polycarbonate-Luggage/dp/B0DXL5G88G/?_encoding=UTF8&pd_rd_w=WeZZh&content-id=amzn1.sym.6ca15ca4-a8c2-4aba-b219-9c4cb936bb3c&pf_rd_p=6ca15ca4-a8c2-4aba-b219-9c4cb936bb3c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/gp/browse.html?node=6648217031&ref_=nav_cs_fashion",
        "https://www.amazon.in/Men-shorts-cotton-casual-Short-11-Lightgrey-L/dp/B0DRFN3SBV/?_encoding=UTF8&pd_rd_w=O5SOC&content-id=amzn1.sym.211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_p=211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_crs_zg_bs_1571271031",
        "https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3F_encoding%3DUTF8%26ref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0",
        "https://www.amazon.in/b/?_encoding=UTF8&node=1380485031&pd_rd_w=U9f7C&content-id=amzn1.sym.f8e82c51-0408-4554-a158-9be4d776850d&pf_rd_p=f8e82c51-0408-4554-a158-9be4d776850d&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/s/?_encoding=UTF8&bbn=1380460031&rh=n%3A1380460031%2Cp_n_format_browse-bin%3A19560802031&pd_rd_w=lou1G&content-id=amzn1.sym.4d494d65-8009-406a-9a50-5e08a16212d7&pf_rd_p=4d494d65-8009-406a-9a50-5e08a16212d7&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/StitchX-Sleeve-Textured-Striped-Cutaway/dp/B0DSWGZGH3/?_encoding=UTF8&pd_rd_w=WeZZh&content-id=amzn1.sym.6ca15ca4-a8c2-4aba-b219-9c4cb936bb3c&pf_rd_p=6ca15ca4-a8c2-4aba-b219-9c4cb936bb3c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/b/?_encoding=UTF8&node=28253258031&ref=ls_gwc_mb_en8_&pd_rd_w=8fN1r&content-id=amzn1.sym.a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_p=a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/PHILIPS-TAE1159BK-00-Earphones-Changeable/dp/B0DL4S61RP/?_encoding=UTF8&pd_rd_w=Sb5ou&content-id=amzn1.sym.049f4884-e005-4b6b-9e95-2b599decd624&pf_rd_p=049f4884-e005-4b6b-9e95-2b599decd624&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/blissbells-Stag-Wall-Lamp-Circle/dp/B0B6CHTKXP/?_encoding=UTF8&pd_rd_w=2le9c&content-id=amzn1.sym.60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_p=60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/Cubiker-Engineered-Multipurpose-Foldable-Ergonomic/dp/B0D53YGZNK/?_encoding=UTF8&pd_rd_w=VC7CT&content-id=amzn1.sym.211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_p=211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_crs_zg_bs_976392031",
        "https://www.amazon.in/Aquaminder-Bottle-Remind-Adults-Perfect/dp/B0DBZL2PTC/?_encoding=UTF8&pd_rd_w=M9gdX&content-id=amzn1.sym.32378808-0263-4069-9a58-814866f75c85&pf_rd_p=32378808-0263-4069-9a58-814866f75c85&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/Asgard-Melt-Blown-Fabric-Disposable-Unisex/dp/B08B1W5QN5/?_encoding=UTF8&pd_rd_w=2le9c&content-id=amzn1.sym.60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_p=60ef2100-df26-49c5-9ae9-41eeccc580aa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/b/?_encoding=UTF8&node=1389396031&pd_rd_w=B35GV&content-id=amzn1.sym.46d2074e-6340-47f1-8d20-54821e9d3161&pf_rd_p=46d2074e-6340-47f1-8d20-54821e9d3161&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://advertising.amazon.in/?ref=Amz.in",
        "https://www.amazon.in/ref=footer_logo",
        "https://www.amazon.in/your-product-safety-alerts?ref_=footer_bsx_ypsa",
        "https://www.amazon.in/b/?node=2838698031&ld=AZINSOANavDesktopFooter_C&ref_=nav_footer_sell_C",
        "https://www.amazon.in/customer-preferences/edit?ie=UTF8&preferencesReturnUrl=%2F&ref_=footer_lang",
        "https://www.aboutamazon.in/?utm_source=gateway&utm_medium=footer",
        "https://www.amazon.in/Fire-Boltt-Smartwatch-Stainless-Resolution-Bluetooth/dp/B0CT3CSYCV/?_encoding=UTF8&pd_rd_w=Sb5ou&content-id=amzn1.sym.049f4884-e005-4b6b-9e95-2b599decd624&pf_rd_p=049f4884-e005-4b6b-9e95-2b599decd624&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/Ambrane-Unbreakable-Charging-Braided-Cable/dp/B098NS6PVG/?_encoding=UTF8&pd_rd_w=VC7CT&content-id=amzn1.sym.211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_p=211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_crs_zg_bs_976392031",
        "https://www.amazon.in/Green-Gainz-Roasted-Assorted-Flavours/dp/B0DSG85V4G/?_encoding=UTF8&pd_rd_w=ZEb4R&content-id=amzn1.sym.0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_p=0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_NSS",
        "https://www.amazon.in/Gourmet-Specialty-Foods/b/?ie=UTF8&node=2454178031&ref_=nav_cs_grocery",
        "https://www.amazon.in/EvoFox-Mechanical-Connectivity-Hot-Swappable-Rechargeable/dp/B0FBRWPD79/?_encoding=UTF8&pd_rd_w=XL4v0&content-id=amzn1.sym.6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_p=6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/b/?_encoding=UTF8&node=28253258031&pd_rd_w=v2LdJ&content-id=amzn1.sym.152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_p=152cfd8e-7a3e-4b37-941e-3cbe5a2e33c3&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/b/?_encoding=UTF8&ie=UTF8&node=4772060031&pd_rd_w=qs3S8&content-id=amzn1.sym.9ff36f11-82d6-4600-a8fb-e52bb32e171c&pf_rd_p=9ff36f11-82d6-4600-a8fb-e52bb32e171c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/ASIAN-Delta-20-Lightweight-Sneakers-Running/dp/B09WLDXXWW/?_encoding=UTF8&pd_rd_w=9A0RW&content-id=amzn1.sym.de84ee3f-a07f-47cd-ac44-50f5d6cbb587&pf_rd_p=de84ee3f-a07f-47cd-ac44-50f5d6cbb587&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_a2i_gw_cml",
        "https://www.audible.in/",
        "https://www.amazon.in/PEXPO-Denim-Blue-Chromo-Xtreme/dp/B0CFF149ZB/?_encoding=UTF8&pd_rd_w=s3S0K&content-id=amzn1.sym.81f4df47-d71a-46ce-b8de-32884f91242b&pf_rd_p=81f4df47-d71a-46ce-b8de-32884f91242b&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.amazon.in/b/?_encoding=UTF8&node=28253258031&ref=ls_gwc_mb_en8_&pd_rd_w=XL4v0&content-id=amzn1.sym.6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_p=6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/s/?_encoding=UTF8&k=zebronics&i=electronics&rh=n%3A976419031%2Cn%3A29561348031%2Cp_89%3AZEBRONICS&pd_rd_w=trRrJ&content-id=amzn1.sym.71850b5e-5657-45e6-935e-feb77b5645a2&pf_rd_p=71850b5e-5657-45e6-935e-feb77b5645a2&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.abebooks.com/",
        "https://www.amazon.in/STRIFF-Adjustable-Patented-Ventilated-Compatible/dp/B07XCM6T4N/?_encoding=UTF8&pd_rd_w=VC7CT&content-id=amzn1.sym.211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_p=211684f4-ebe1-443f-8a4a-0773471e979f&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_crs_zg_bs_976392031",
        "https://www.amazon.in/s/?_encoding=UTF8&k=noise&i=electronics&rh=n%3A1388921031%2Cp_n_condition-type%3A8609960031%2Cp_36%3A-200000&pd_rd_w=trRrJ&content-id=amzn1.sym.71850b5e-5657-45e6-935e-feb77b5645a2&pf_rd_p=71850b5e-5657-45e6-935e-feb77b5645a2&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/s/?_encoding=UTF8&i=home-improvement&rh=n%3A87322479031%2Cp_36%3A-29900%2Cp_72%3A1318476031&dc=&fs=true&qid=1714750891&rnid=1318475031&ref=sr_nr_p_72_1&ds=v1%3AKT2aFWvve4xsaDjrU17ctKHJFfdbS%2FW1Ex2L5A6belw&pd_rd_w=plRzf&content-id=amzn1.sym.0a250fc6-18a4-49da-8c15-ae7cde5579f2&pf_rd_p=0a250fc6-18a4-49da-8c15-ae7cde5579f2&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk", 
        "https://www.amazon.in/s/?_encoding=UTF8&i=electronics&bbn=1388921031&rh=n%3A1388921031%2Cp_89%3ABoult&pd_rd_w=CzJp8&content-id=amzn1.sym.82b20790-8877-4d70-8f73-9d8246e460aa&pf_rd_p=82b20790-8877-4d70-8f73-9d8246e460aa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/ref=nav_logo",
        "https://www.amazon.in/gp/site-directory?ref_=nav_em_js_disabled",
        "https://www.amazon.in/QONETIC-Layer-Adjustable-Stand-Collapsible/dp/B0DNN46SBK/?_encoding=UTF8&pd_rd_w=8fN1r&content-id=amzn1.sym.a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_p=a54e8247-6244-40a3-9737-4a35005be78e&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazonpay.in/merchant",
        "https://sell.amazon.in/grow-your-business/amazon-global-selling.html?ld=AZIN_Footer_V1&ref=AZIN_Footer_V1",
        "https://www.amazon.in/Slyford-Leak-Proof-Dispenser-Silicon-Vinegar/dp/B0BF6293VR/?_encoding=UTF8&pd_rd_w=s3S0K&content-id=amzn1.sym.81f4df47-d71a-46ce-b8de-32884f91242b&pf_rd_p=81f4df47-d71a-46ce-b8de-32884f91242b&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_LPDEALS",
        "https://www.imdb.com/",
        "https://www.amazon.in/b/?_encoding=UTF8&node=4286640031&pd_rd_w=plRzf&content-id=amzn1.sym.0a250fc6-18a4-49da-8c15-ae7cde5579f2&pf_rd_p=0a250fc6-18a4-49da-8c15-ae7cde5579f2&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/EvoFox-Falcon-X85-Multifunctional-Textured/dp/B08QV7BQHZ/?_encoding=UTF8&pd_rd_w=XL4v0&content-id=amzn1.sym.6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_p=6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://services.amazon.in/services/fulfilment-by-amazon/benefits.html/ref=az_footer_fba?ld=AWRGINFBAfooter",
        "https://www.amazon.in/deals?ref_=nav_cs_gb",
        "https://www.amazon.in/s/?_encoding=UTF8&bbn=21541481031&rh=n%3A21541481031%2Cp_72%3A1318477031&pd_rd_w=qs3S8&content-id=amzn1.sym.9ff36f11-82d6-4600-a8fb-e52bb32e171c&pf_rd_p=9ff36f11-82d6-4600-a8fb-e52bb32e171c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/electronics/b/?ie=UTF8&node=976419031&ref_=nav_cs_electronics",
        "https://www.amazon.in/Car-Motorbike-Store/b/?ie=UTF8&node=4772060031&ref_=nav_cs_automotive",
        "https://www.amazon.in/Sony-DualSense-Wireless-Controller-PlayStation/dp/B0BMPLHLZ9/?_encoding=UTF8&pd_rd_w=XL4v0&content-id=amzn1.sym.6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_p=6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/now?ref=footer_amznow",
        "https://www.amazon.in/customer-preferences/country?ie=UTF8&preferencesReturnUrl=%2F&ref_=footer_icp_cp",
        "https://www.amazon.in/KTM-Ebony-Black-Booking-Ex-Showroom/dp/B0F5399MQN/?_encoding=UTF8&pd_rd_w=TIgqP&content-id=amzn1.sym.c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_p=c85ce2dc-2c4b-42b3-8150-5574e717462c&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en4_",
        "https://www.amazon.in/gp/redirect.html/ref=footer_twitter?location=http://twitter.com/AmazonIN&token=A309DFBFCB1E37A808FF531934855DC817F130B6&6",
        "https://www.amazon.in/Prep-Glint-Anti-Hair-Botanical-Clinically/dp/B0FF2HYDLW/?_encoding=UTF8&pd_rd_w=ZEb4R&content-id=amzn1.sym.0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_p=0b9f88e1-0d74-4adf-ac95-3a06477a8aaa&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_NSS",
        "https://press.aboutamazon.in/?utm_source=gateway&utm_medium=footer",
        "https://www.amazon.in/Montra-Chord-Geared-Black-1FPQ36G0C07000A/dp/B09V13LJ2V/?_encoding=UTF8&pd_rd_w=Qcztg&content-id=amzn1.sym.10fbb0e8-f7f0-4de9-bee0-d6ae0d1b703e&pf_rd_p=10fbb0e8-f7f0-4de9-bee0-d6ae0d1b703e&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/gcx/-/gfhz/?ref_=nav_cs_giftfinder",
        "https://www.amazon.in/Decorcity-Electric-Operated-Artificial-Valentines/dp/B0DJ1R3LLL/?_encoding=UTF8&pd_rd_w=3Rle5&content-id=amzn1.sym.91b7b9d8-d2b8-4319-9dd3-9b1005242396&pf_rd_p=91b7b9d8-d2b8-4319-9dd3-9b1005242396&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/s/?_encoding=UTF8&i=fashion&bbn=90505325031&rh=n%3A6648217031%2Cn%3A90418239031%2Cn%3A90505325031%2Cn%3A7459780031%2Cn%3A1953602031%2Cn%3A11400137031%2Cn%3A1968542031%2Cp_85%3A10440599031&hidden-keywords=-sponsored-men&pd_rd_w=uoDz3&content-id=amzn1.sym.1350f669-3050-4d58-9819-7ff3e03b8408&pf_rd_p=1350f669-3050-4d58-9819-7ff3e03b8408&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_unk",
        "https://www.amazon.in/Home-Kitchen/b/?ie=UTF8&node=976442031&ref_=nav_cs_home",
        #"https://www.amazon.in/s/?_encoding=UTF8&bbn=84514735031&rh=n%3A84514735031%2Cp_85%3A10440599031&pd_rd_w=HrZc4&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        #"https://www.amazon.in/s/?_encoding=UTF8&bbn=84514739031&rh=n%3A84514739031%2Cp_85%3A10440599031&pd_rd_w=HrZc4&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=4WBM0N8"https://www.amazon.in/Decorcity-Electric-Operated-Artificial-Valentines/dp/B0DJ1R3LLL/?_encoding=UTF8&pd_rd_w=3Rle5&content-id=amzn1.sym.91b7b9d8-d2b8-4319-9dd3-9b1005242396&pf_rd_p=91b7b9d8-d2b8-4319-9dd3-9b1005242396&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/s/?_encoding=UTF8&i=fashion&bbn=90505325031&rh=n%3A6648217031%2Cn%3A90418239031%2Cn%3A90505325031%2Cn%3A7459780031%2Cn%3A1953602031%2Cn%3A11400137031%2Cn%3A1968542031%2Cp_85%3A10440599031&hidden-keywords=-sponsored-men&pd_rd_w=uoDz3&content-id=amzn1.sym.1350f669-3050-4d58-9819-7ff3e03b8408&pf_rd_p=1350f669-3050-4d58-9819-7ff3e03b8408&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_unk",
        "https://www.amazon.in/Home-Kitchen/b/?ie=UTF8&node=976442031&ref_=nav_cs_home",
        "https://www.amazon.in/s/?_encoding=UTF8&bbn=84514735031&rh=n%3A84514735031%2Cp_85%3A10440599031&pd_rd_w=HrZc4&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        #"https://www.amazon.in/s/?_encoding=UTF8&bbn=84514739031&rh=n%3A84514739031%2Cp_85%3A10440599031&pd_rd_w=HrZc4&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=4WBM0N8"https://www.amazon.in/Home-Kitchen/b/?ie=UTF8&node=976442031&ref_=nav_cs_home",
        "https://www.amazon.in/s/?_encoding=UTF8&bbn=84514735031&rh=n%3A84514735031%2Cp_85%3A10440599031&pd_rd_w=HrZc4&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/s/?_encoding=UTF8&bbn=84514739031&rh=n%3A84514739031%2Cp_85%3A10440599031&pd_rd_w=HrZc4&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/s/?_encoding=UTF8&bbn=84514739031&rh=n%3A84514739031%2Cp_85%3A10440599031&pd_rd_w=HrZc4&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=fQYst&pd_rd_r=fbf1b194-14d8-4c1a-855b-bbd01a2f0fa0&ref_=pd_hp_d_atf_unk",
        "https://www.amazon.in/AMKETTE-Amkette-Fireblade-Keyboard-Anti-Ghosting/dp/B085366TJW/?_encoding=UTF8&pd_rd_w=XL4v0&content-id=amzn1.sym.6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_p=6367b31e-8ef8-40a2-9ad2-2e232c8ee0dd&pf_rd_r=4WBM0N8Y0QFYC3WBZXP4&pd_rd_wg=eB1UU&pd_rd_r=647cec79-1e46-42ac-80dd-a79eccc85f06&ref_=pd_hp_d_btf_ls_gwc_pc_en2_",
        "https://www.amazon.in/Audible-Books-and-Originals/b/?ie=UTF8&node=17941593031&ref_=nav_cs_audible",
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
'''   
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

'''
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
            #flipkart_deals = fetch_flipkart_loot_deals()
            #all_deals.extend(flipkart_deals)
            
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