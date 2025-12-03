# ExoMarket

Django e-commerce project where users can buy and sell exotic items:


### **Project Overview:**
An e-commerce platform where authenticated users can list, buy, and sell exotic items. The application will have user registration, item listing, cart functionality

### **Features:**
1. **User Authentication:**
   - Registration, login, and profile management using Django’s built-in authentication system with an abstract user model.
   - Extra fields: phone number and age.

2. **Item Management:**
   - Users can create, update, and delete items.
   - Items have attributes like name, description, price, image, and category.

3. **Shopping Cart:**
   - Users can add items to their cart.
   - Cart management with options to view, update, or remove items.


### **Detailed Components:**

#### **Models:**
1. **Custom User Model (`User`):**
   - Fields: username, email, password, phone number, age, etc.

2. **Item Model (`Item`):**
   - Fields: name, description, price, image, category, seller (ForeignKey to User), available (Boolean).

3. **Cart Model (`Cart`):**
   - Fields: user (OneToOne with User), items (ManyToMany with Item), total_price.

4. **Transaction Model (`Transaction`):**
   - Fields: buyer, seller, item, transaction_date, status.

#### **Forms:**
1. **User Registration Form:** For creating new users with extra fields.
2. **User Update Form:** For updating user information.
3. **Item Form:** For creating and updating item listings.
4. **Cart Update Form:** For adding/removing items from the cart.

#### **Views:**
1. **Authentication Views:**
   - Register, login, logout, profile update.

2. **Item Views:**
   - Create, update, list items.
   - Item detail view.

3. **Cart Views:**
   - Add to cart, view cart, update cart.


#### **Templates (HTML, CSS, JavaScript):**
- **Home Page:** Display featured and latest items.
- **Item Listing Page:** Show all items with filters and search.
- **Item Detail Page:** Detailed view of an item with an option to add to cart.
- **Cart Page:** View and update items in the cart.
- **User Profile:** Update profile information.

### **Implementation Steps:**
1. **Set Up Django Project:** Install Django, create a new project and app.
2. **Custom User Model:** Create an abstract user model with extra fields.
3. **Create Models and Migrations:** Define models with relationships and run migrations.
4. **Develop Forms:** Create forms for user registration, item creation, and updates.
5. **Build Views:** Implement views to handle CRUD operations for users and items.
6. **Design Templates:** Use HTML, CSS, and JavaScript for front-end design.
8. **Testing:** Test all features for bugs and usability.

