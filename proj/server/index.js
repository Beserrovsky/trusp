const { MongoClient } = require('mongodb');
const mqtt = require('async-mqtt');

const db_uri =
  'mongodb://localhost:27017';

const mqtt_uri = 
  'mqtt://broker.hivemq.com';

// Topic for db warnings
const WRN_TOPIC = 'TRUSP-db';

const SUBS = {'TRUSP-led': {qos: 0}, 'TRUSP-dht': {qos: 1}};

async function db_conn() {
  try {
    await db_client.connect();

    await db_client.db('admin').command({ ping: 1 });
    console.log('Connected successfully to mongodb server!');
  } finally { }
}

async function mqtt_conn() {
  try {
    client = await mqtt.connectAsync(mqtt_uri);
    
    console.log('Connected successfully to mqtt broker!');

    return client;
  } finally { }
}

async function handleMsg(topic, msg) {
  console.log(msg.toString());
}

const db_client = new MongoClient(db_uri);

async function main() {
  
  // Connect to MongoDB
  await db_conn().catch(console.dir);

  // Connect to broker
  const client = await mqtt_conn().catch(console.dir);

  // Set cb
  await client.on('message', handleMsg);

  // Subscribes to topics
  await client.subscribe(SUBS, (err) => err? console.error : null);

  // Warning database recording
  await client.publish(WRN_TOPIC, 'Database recording started!');

  process.on('SIGINT', async () => {

    // Closes conn to broker
    await client.end();
  
    // Closes conn to MongoDB
    await db_client.close();

    console.log("\nTill next time, see ya!!!");
  });
}

main();
