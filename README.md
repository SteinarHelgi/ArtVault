# ArtVault
Verklegt 2

# Extra Requirements
- Search by artist in the artwork catalogue
- Order artwork by artist
- View art movements with descriptions and featured artworks
- View information pages for movement artists / famous artists
- Separate account types for buyers, individual sellers, and galleries
- Separate signup and setup flows depending on account type
- Public seller profile pages
- Private seller dashboard for managing profile and listings
- Sellers can create, update, and delete listings
- Sellers can view bids placed on their own listings, including bidder name and bid amount
- Automatic auction closing when an artwork reaches its auction end date
- Automatic acceptance of the highest bid when the auction closes
- Minimum bid restriction requiring bids to be at least 10% above the current highest bid
- View all sellers page
- View all artists page
- Loading screen
- Footer with links
- Order summary on every finalize-bid step
- Pagination on the browse artwork page
- Homepage artwork sections grouped by art movement 
- Homepage artworks are unsold
- Side scrolling artwork showcases
- Full-screen preview of artwork image viewer on artwork detail pages
- Live preview for image uploads
- Password change inside account settings
- Listing validation for auction dates
- Listing validation limiting uploaded artwork images
- About us in footer. Short description about the website 
- Common questions in footer. Answer to possible problems users might run into
- Terms and conditions in footer

# Instructions
1. unzip the directory
2. Create a virtual enviornment (venv)
3. Then install the requirements using
   ```bash
   pip install -r "requirements.txt"
   ```
4. Make sure that the .env file has a SERVER_PASSWORD variable.
5. start the server using python3 manage.py runserver

# Test Accounts login:


## Buyer account
Username: BuyerTest

Password: Password123!"#

## Individual seller account
Username: IndividualSellerTest

Password: Password123!"#

## Gallery account
Username: GalleryTest

Password: Password123!"#



