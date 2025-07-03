// Get environment variables or use defaults
const rootUsername = process.env.MONGO_INITDB_ROOT_USERNAME;
const rootPassword = process.env.MONGO_INITDB_ROOT_PASSWORD;
const databaseName = process.env.MONGO_INITDB_DATABASE;

db = db.getSiblingDB("admin");
db.auth(rootUsername, rootPassword);

db = db.getSiblingDB(databaseName);
db.createUser({
  user: rootUsername,
  pwd: rootPassword,
  roles: [{ role: "readWrite", db: databaseName }],
});
