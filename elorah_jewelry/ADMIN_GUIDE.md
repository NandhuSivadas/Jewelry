# Elorah Jewellery - Admin Panel Guide

Welcome to the Elorah Admin Panel! This interface is the central nervous system of your e-commerce store. Because we've integrated the modern **Unfold** theme, it looks clean and luxurious, perfectly matching your brand.

Here is a detailed breakdown of every section in your left sidebar, what it does, and how you should use it day-to-day.

---

## 1. Catalog (Your Storefront)
This is where you manage everything the customer actually sees and buys.

- **Categories:** 
  Organize your store (e.g., "Necklaces", "Bridal", "Rings"). 
  *Tip:* If you upload an image here, it automatically appears in the circular scrolling marquee and the "Our Collections" square bento grid on the homepage!
  
- **Materials & Purities:** 
  Define the base metals of your jewelry (e.g., "Gold", "Silver", "AD Stone") and their purity levels (e.g., "22K", "925"). These are used for filtering and dynamic price calculations.
  
- **Products:** 
  The core of your store. Here you add new jewelry pieces, set their base prices (or mark them as "Price on Request"), assign them to categories, and upload their images. 
  *Tip:* Check the **"Is new arrival"** box to make the product instantly appear in the *Latest Collections* section on the homepage. Check **"Is featured"** to put it in the *Most Loved* scrolling carousel.

---

## 2. Promotions (Marketing)
Control sales, banners, and discounts.

- **Banners:** 
  Control the massive Hero section at the top of your homepage. You can upload an image or an MP4 video here. Ensure "Position" is set to "Main hero slider" and "Is active" is checked.
  
- **Coupons:** 
  Create discount codes (e.g., "DIWALI15"). You can set them to be a flat amount (₹500 off) or a percentage (15% off). You can also restrict them to specific categories or set a minimum order value.
  
- **Coupon Usages:** 
  A tracking page. It shows you exactly which customer used which coupon on which order.

---

## 3. Orders & Cart (Fulfillment)
Where the business happens.

- **Orders:** 
  When a customer buys something, it appears here. You can click into an order to see their shipping address, what they bought, the total price, and update the **Order Status** (e.g., move it from "Pending" to "Shipped").
  
- **Carts & Cart Items:** 
  View what active customers currently have sitting in their shopping carts. Useful for analytics or seeing what products are highly desired but not being checked out.

---

## 4. Payments (Financials)
Track the money.

- **Transactions:** 
  Logs of every payment attempt made through your payment gateway (e.g., Razorpay/Stripe). You can see if a payment was successful, failed, or refunded.
  
- **Refunds:** 
  Manage money sent back to customers for cancelled or returned orders.

---

## 5. Pricing (Dynamic Calculation)
Advanced controls for your gold rates.

- **Metal Rates:** 
  If you are using dynamic pricing (where jewelry prices fluctuate with the daily market price of gold), you update the daily rate here. Changing the rate here instantly recalculates the final price of all dynamic products across the entire website.
  
- **GST Configurations:** 
  Manage tax brackets (e.g., 3% for Gold Jewellery) applied at checkout.
  
- **Shipping Zones:** 
  Define delivery fees based on pincodes or states.

---

## 6. Accounts (User Management)
Manage the people interacting with your site.

- **Users:** 
  Your customer database. You can see their emails, when they joined, and whether they are active. You can also grant trusted employees "Staff status" here so they can log into this admin panel.
  
- **Groups:** 
  Create permission levels. For example, you could create an "Inventory Manager" group that can only add Products, but cannot see Financials or Orders.

---

## 7. Reviews & Wishlist (Engagement)
Monitor customer interaction.

- **Product Reviews:** 
  When customers leave a star rating and comment on a product, it lands here. You can moderate them (approve or hide them) before they appear publicly in the "Stories of Joy" section on the homepage.
  
- **Wishlists:** 
  See which products customers are saving for later. Highly useful for deciding what to put on sale!

---

## 8. Audit & Security (Logs)
Keep your store safe.

- **Audit Logs:** 
  A master security ledger. It records exactly *who* changed *what* and *when*. If a product price gets changed accidentally, you can check here to see which employee account did it.
  
- **Access Attempts/Failures (Axes):** 
  Security logs showing failed login attempts to the admin panel. Helps you spot if someone is trying to guess your passwords.
  
- **OTP/TOTP Devices:** 
  Two-factor authentication settings for your staff accounts.

---

## 9. Periodic Tasks (Celery)
Advanced automation.

- **Periodic Tasks / Crontabs:** 
  If you set up background tasks (like automatically emailing customers who abandoned their carts after 24 hours, or auto-fetching daily gold rates from an API), they are scheduled and monitored here.
