// Define the database structure using DBML (Database Markup Language)
// Documentation: https://dbml.dbdiagram.io/docs


// Table to store user details
Table Users {
  id uuid [primary key, increment] // Unique identifier for the user
  name varchar(255) // Full name of the user
  email varchar(255) [unique] // E-mail of the user
  hashed_passowrd varchar(255) // Password hashed
  created_at timestamp [default: `now()`] // Date when the user are created
  updated_at timestamp [default: `now()`] // Date when the user are updated
  deleted_at timestamp [default: `now()`] // Date when the user are deleted
}

// Table to record wishlist products
Table Wishlist {
  id uuid // Unique identifier for the row
  user_id	uuid // User id foreign key
  product_id	uuid // product_id of the api
  created_at timestamp [default: `now()`] // Date when the product of a the are created
  deleted_at timestamp [default: `now()`] // Date when the product of a the are deleted

  indexes {
    (product_id, user_id) [unique]
  }
}


// Define references between tables
Ref: Users.id > Wishlist.id
