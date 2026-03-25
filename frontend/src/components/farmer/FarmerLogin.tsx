/** Farmer login screen with phone number + OTP flow. */

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";

type Step = "phone" | "otp" | "register";

/** Phone + OTP login flow for farmers. */
export function FarmerLogin() {
  const navigate = useNavigate();
  const { sendOTP, verifyCode, isLoading, error } = useAuth();

  const [step, setStep] = useState<Step>("phone");
  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState("");
  const [devOtp, setDevOtp] = useState("");
  const [fullName, setFullName] = useState("");

  const handleSendOTP = async () => {
    const code = await sendOTP(phone);
    if (code) {
      setDevOtp(code);
      setStep("otp");
    }
  };

  const handleVerifyOTP = async () => {
    const result = await verifyCode(phone, otp, fullName || undefined);
    if (result) {
      if (result.is_new_user) {
        setStep("register");
      } else {
        navigate("/farmer");
      }
    }
  };

  const handleRegisterComplete = async () => {
    const result = await verifyCode(phone, otp, fullName);
    if (result) {
      navigate("/farmer");
    }
  };

  return (
    <div className="min-h-screen bg-surface flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="font-display text-3xl text-primary mb-2">CropFolio</h1>
          <p className="text-text-secondary font-myanmar text-lg">
            သင့်လယ်ယာအတွက် အကောင်းဆုံး အကြံပြုချက်
          </p>
          <p className="text-text-tertiary text-sm mt-1">
            Smart farming recommendations
          </p>
        </div>

        {/* Phone step */}
        {step === "phone" && (
          <div className="space-y-4">
            <label className="block">
              <span className="text-text-secondary text-sm font-myanmar">
                ဖုန်းနံပါတ်
              </span>
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="+959123456789"
                className="mt-1 block w-full rounded-lg bg-surface-elevated border border-border px-4 py-3 text-text-primary text-lg focus:border-primary focus:outline-none"
                style={{ fontSize: "16px" }}
              />
            </label>
            <button
              onClick={handleSendOTP}
              disabled={isLoading || phone.length < 8}
              className="w-full py-3 rounded-lg bg-primary text-white font-semibold text-lg disabled:opacity-50 min-h-[48px]"
            >
              {isLoading ? "Sending..." : "OTP ပို့ပါ"}
            </button>
          </div>
        )}

        {/* OTP step */}
        {step === "otp" && (
          <div className="space-y-4">
            <label className="block">
              <span className="text-text-secondary text-sm font-myanmar">
                OTP ကုဒ် ထည့်ပါ
              </span>
              <input
                type="text"
                inputMode="numeric"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                placeholder="000000"
                maxLength={6}
                className="mt-1 block w-full rounded-lg bg-surface-elevated border border-border px-4 py-3 text-text-primary text-center text-2xl tracking-[0.5em] focus:border-primary focus:outline-none"
                style={{ fontSize: "24px" }}
              />
            </label>
            {devOtp && (
              <p className="text-xs text-text-tertiary text-center">
                Dev OTP: <code className="text-accent">{devOtp}</code>
              </p>
            )}
            <label className="block">
              <span className="text-text-secondary text-sm font-myanmar">
                အမည် (ပထမဆုံးအကြိမ်ဖြစ်ပါက)
              </span>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="U Kyaw Zin"
                className="mt-1 block w-full rounded-lg bg-surface-elevated border border-border px-4 py-3 text-text-primary focus:border-primary focus:outline-none"
                style={{ fontSize: "16px" }}
              />
            </label>
            <button
              onClick={handleVerifyOTP}
              disabled={isLoading || otp.length !== 6}
              className="w-full py-3 rounded-lg bg-primary text-white font-semibold text-lg disabled:opacity-50 min-h-[48px]"
            >
              {isLoading ? "Verifying..." : "အတည်ပြုပါ"}
            </button>
            <button
              onClick={() => setStep("phone")}
              className="w-full py-2 text-text-tertiary text-sm"
            >
              ဖုန်းနံပါတ် ပြောင်းရန်
            </button>
          </div>
        )}

        {/* Register step (first-time user) */}
        {step === "register" && (
          <div className="space-y-4">
            <p className="text-text-secondary font-myanmar text-center">
              ကြိုဆိုပါတယ်! သင့်အမည်ထည့်ပါ
            </p>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="အမည်အပြည့်အစုံ"
              className="block w-full rounded-lg bg-surface-elevated border border-border px-4 py-3 text-text-primary font-myanmar focus:border-primary focus:outline-none"
              style={{ fontSize: "16px" }}
            />
            <button
              onClick={handleRegisterComplete}
              disabled={isLoading || !fullName.trim()}
              className="w-full py-3 rounded-lg bg-primary text-white font-semibold text-lg disabled:opacity-50 min-h-[48px]"
            >
              {isLoading ? "..." : "စတင်ပါ"}
            </button>
          </div>
        )}

        {error && (
          <p className="mt-4 text-center text-danger text-sm">{error}</p>
        )}
      </div>
    </div>
  );
}
