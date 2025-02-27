interface ApiResponse {
  message: string;
  hash?: string;
  success?: boolean;
  exists?: boolean;
  validation?: boolean;
}

const API_BASE_URL = "https://pxlproof.ashwinshome.co.uk/api";

export const uploadImage = async (
  endpoint: "publish" | "verify" | "check",
  file: File
): Promise<ApiResponse> => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
      method: "POST",
      headers: {
        accept: "application/json",
      },
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || `HTTP error! status: ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error(`Error in ${endpoint} request:`, error);
    throw error;
  }
};
