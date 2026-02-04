Built a full-stack booking and payment backend with Django REST Framework, JWT authentication, Razorpay integration(soon), and role-based access control.

StayHub – Hotel / PG / Hostel Booking Platform (Django, DRF, JWT, Razorpay)

Designed and developed a role-based SaaS backend for property listing, room management, bookings, and payments using Django REST Framework.
Implemented JWT authentication with role-based permissions (Customer, Vendor, Admin) to secure APIs.
Built a booking engine with atomic transactions to prevent overbooking and ensure availability consistency.
Designed room-level inventory management with real-time availability tracking.
Integrated Razorpay payments using server-side order creation and secure webhook verification.
Implemented payment retry logic and booking lifecycle management.
Developed vendor dashboard APIs using aggregate queries to track bookings and revenue.
Client (Frontend)
     |
     v
API Gateway (DRF + JWT)
     |
     v
Business Logic Layer
(Property / Room / Booking / Payment)
     |
     v
Database (PostgreSQL / MySQL)
     |
     v
External Service (Razorpay Webhooks)

<img width="1920" height="1080" alt="Screenshot (358)" src="https://github.com/user-attachments/assets/1b2cb274-b81a-404f-bc01-9cf638017e27" />
<img width="1920" height="1080" alt="Screenshot (359)" src="https://github.com/user-attachments/assets/95636120-574b-44e1-b806-387e80ba9761" />
<img width="1920" height="1080" alt="Screenshot (360)" src="https://github.com/user-attachments/assets/b6134b80-70b2-4356-967c-ea46b8722122" />
<img width="1920" height="1080" alt="Screenshot (361)" src="https://github.com/user-attachments/assets/427c2014-fd6f-4f2a-9784-40cc9de5c0d9" />
<img width="1920" height="1080" alt="Screenshot (362)" src="https://github.com/user-attachments/assets/3549582e-44a8-4dfd-88c4-1f890ccc3868" />
<img width="1920" height="1080" alt="Screenshot (363)" src="https://github.com/user-attachments/assets/4f4449b3-6e2b-407c-adb0-c68932540036" />







