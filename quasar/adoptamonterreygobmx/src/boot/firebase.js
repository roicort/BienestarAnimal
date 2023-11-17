import {initializeApp} from 'firebase/app';
import {getAnalytics} from 'firebase/analytics';
import {getFirestore} from 'firebase/firestore';
import {getStorage} from 'firebase/storage';
import {getAuth} from 'firebase/auth';

const firebaseConfig = {
  apiKey: 'AIzaSyBKjAp_Dyb3QuZRBLi7bxUigxJQ4D4p4-c',
  authDomain: 'adoptamos.web.app',
  projectId: 'id-mty',
  storageBucket: 'id-mty.appspot.com',
  messagingSenderId: '795395350214',
  appId: '1:795395350214:web:db49269c260a661f1101c7',
  measurementId: 'G-6TZLL3K6N5'
};


const firebaseApp = initializeApp(firebaseConfig);
const firebaseAuth = getAuth(firebaseApp);
const firestoreDB = getFirestore(firebaseApp);
const firebaseStorage = getStorage(firebaseApp);
const firbaseAnalytics = getAnalytics(firebaseApp);

export {firestoreDB, firebaseAuth, firebaseStorage, firebaseApp, firbaseAnalytics};
