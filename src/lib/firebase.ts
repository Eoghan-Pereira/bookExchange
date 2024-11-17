// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics, isSupported } from "firebase/analytics";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAjJCqDovFH7LoNentcX06RJhuzbp90Q_4",
  authDomain: "ecommerce-69ea5.firebaseapp.com",
  projectId: "ecommerce-69ea5",
  storageBucket: "ecommerce-69ea5.firebasestorage.app",
  messagingSenderId: "134087122858",
  appId: "1:134087122858:web:0a22e366c98767ca3395d3",
  measurementId: "G-VPSYF1Q2SR"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

async function initAnalytics() {
  if (await isSupported()) {
    const analytics = getAnalytics(app);
  } else {
    console.log('Firebase Analytics is not supported in this environment.');
  }
}

if (typeof window !== 'undefined') {
  initAnalytics();
}

export { app, auth };