import {initializeApp} from 'firebase/app';
import {getAnalytics} from 'firebase/analytics';
import {getFirestore} from 'firebase/firestore';
import {getStorage} from 'firebase/storage';
import {getAuth} from 'firebase/auth';

const firebaseConfig = {
  apiKey: 'AIzaSyDzZI8kumZqOShHQaTrzbwNaA0JiEMwg7M',
  authDomain: 'adoptamos.web.app',
  projectId: 'mty-id-dev',
  storageBucket: 'mty-id-dev.appspot.com',
  messagingSenderId: '149828993345',
  appId: '1:149828993345:web:11757472dbff01d7ebe1c0',
  measurementId: 'G-F293PRW558'
};

const firebaseApp = initializeApp(firebaseConfig);
const firebaseAuth = getAuth(firebaseApp);
const firestoreDB = getFirestore(firebaseApp);
const firebaseStorage = getStorage(firebaseApp);
const firbaseAnalytics = getAnalytics(firebaseApp);

export {firestoreDB, firebaseAuth, firebaseStorage, firebaseApp, firbaseAnalytics};
