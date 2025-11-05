
db = db.getSiblingDB("admin");

// Création des rôles
db.createRole({
  role: "reader",
  privileges: [
    { resource: { db: "hcare_db", collection: "" }, actions: ["find"] }
  ],
  roles: []
});

db.createRole({
  role: "writer",
  privileges: [
    { resource: { db: "hcare_db", collection: "" }, actions: ["insert", "update", "remove", "find"] }
  ],
  roles: []
});

db.createRole({
  role: "admin",
  privileges: [
    { resource: { db: "hcare_db", collection: "" }, actions: ["find", "insert", "update", "remove", "dropCollection", "createCollection","createIndex","viewUser"] },
    { resource: { db: "admin", collection: "" }, actions: ["createUser","dropUser", "grantRole", "revokeRole","viewRole","viewUser"] }
  ],
  roles: []
});

// Création des utilisateurs
db.getSiblingDB("hcare_db").createUser({
  user: "readerUser",
  pwd: "readerPassword",
  roles: [{ role: "reader", db: "admin" }]
});

db.getSiblingDB("hcare_db").createUser({
  user: "writerUser",
  pwd: "writerPassword",
  roles: [{ role: "writer", db: "admin" }]
});

db.getSiblingDB("admin").createUser({
  user: "adminUser",
  pwd: "adminPassword",
  roles: [{ role: "admin", db: "admin" }]
});

print("Users created!");