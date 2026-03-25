/** Authentication types for the B2B2C platform. */

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user_id: string;
  role: "farmer" | "distributor" | "admin";
  is_new_user: boolean;
}

export interface UserProfile {
  id: string;
  phone_number: string | null;
  email: string | null;
  role: string;
  full_name: string;
  full_name_mm: string | null;
  preferred_language: string;
  township_id: string | null;
  organization_id: string | null;
}
