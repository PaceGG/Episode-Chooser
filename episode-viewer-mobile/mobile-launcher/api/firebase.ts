import { initializeApp, getApps, getApp } from "firebase/app";
import {
  getDatabase,
  ref,
  onValue,
  set,
  push,
  update,
  remove,
  child,
  get,
} from "firebase/database";

const firebaseConfig = {
  databaseURL:
    "https://episode-chooser-a0459-default-rtdb.asia-southeast1.firebasedatabase.app/",
};

const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();
const database = getDatabase(app);

export { database, ref, onValue, set, push, update, remove, child, get };
