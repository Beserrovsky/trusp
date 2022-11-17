const { MongoClient } = require('mongodb');
const mqtt = require('async-mqtt');

// Topic for db warnings
const WRN_TOPIC = 'TRUSP-db';

// Database Name
const DB_NAME = 'TRUSP';

const db_uri =
  'mongodb://localhost:27017/' + DB_NAME;

const mqtt_uri = 
  'mqtt://broker.hivemq.com';

const SUBS = {'TRUSP-itn': {qos: 0}, 'TRUSP-temp': {qos: 0}, 'TRUSP-hum': {qos: 0}};

async function db_conn() {
  try {
    await db_client.connect();

    let dbo = db_client.db(DB_NAME);

    dbo.command({ ping: 1 });

    console.log('Connected successfully to mongodb server!');
    
    return dbo;
  } finally { }
}

async function mqtt_conn() {
  try {
    client = await mqtt.connectAsync(mqtt_uri);
    
    console.log('Connected successfully to mqtt broker!');

    return client;
  } finally { }
}

async function handleMsg(topic, msg, dbo) {
  msg = msg.toString();

  console.log(`Message received on "${topic}": ${msg.toString()}`);

  let doc;

  // Save to Database
  switch(topic) {
    case 'TRUSP-itn':
      doc = {
        itensity: Number(msg),
        timestamp: Date.now()
      }

      await saveDoc(doc, 'itn', dbo);
      break;
    case 'TRUSP-temp':
      doc = {
        temperature: Number(msg),
        timestamp: Date.now()
      }

      await saveDoc(doc, 'temp', dbo);
      break;
    case 'TRUSP-hum':
      doc = {
        humidity: Number(msg),
        timestamp: Date.now()
      }

      await saveDoc(doc, 'hum', dbo);
      break;
  }

}

const saveDoc = async (doc, collection, dbo) => {
  let col = dbo.collection(collection);
  const result = await col.insertOne(doc);
  console.log(
    `A ${collection} document was inserted with the _id: ${result.insertedId}`,
  );
}

const db_client = new MongoClient(db_uri);

async function main() {
  
  // Connect to MongoDB
  let dbo = await db_conn().catch(console.dir);

  // Connect to broker
  const client = await mqtt_conn().catch(console.dir);

  // Set cb
  await client.on('message', (topic, msg) => handleMsg(topic, msg, dbo));

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
