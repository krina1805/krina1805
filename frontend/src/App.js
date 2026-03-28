import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import HealthcareChat from "./pages/HealthcareChat";
import JobApplication from "./pages/JobApplication";
import SupportChat from "./pages/SupportChat";
import FeedbackForm from "./pages/FeedbackForm";
import AppointmentBooking from "./pages/AppointmentBooking";
import CustomerServiceChat from "./pages/CustomerServiceChat";
import { Toaster } from "./components/ui/sonner";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/healthcare" element={<HealthcareChat />} />
          <Route path="/job-application" element={<JobApplication />} />
          <Route path="/support" element={<SupportChat />} />
          <Route path="/feedback" element={<FeedbackForm />} />
          <Route path="/appointments" element={<AppointmentBooking />} />
          <Route path="/customer-service" element={<CustomerServiceChat />} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-center" />
    </div>
  );
}

export default App;