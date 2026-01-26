/**
 * Utility function to safely convert error responses to strings
 * Handles various error formats including FastAPI/Pydantic validation errors and network errors
 */
export function formatErrorMessage(error: any): string {
  // Handle different types of error responses
  let errorMessage = 'An error occurred';

  if (error?.response?.data?.detail) {
    // Standard error message
    errorMessage = typeof error.response.data.detail === 'string'
      ? error.response.data.detail
      : JSON.stringify(error.response.data.detail);
  } else if (error?.response?.data) {
    // Check if it's a validation error object with msg property
    if (typeof error.response.data === 'object' && error.response.data.msg) {
      errorMessage = error.response.data.msg;
    } else {
      errorMessage = JSON.stringify(error.response.data);
    }
  } else if (error?.request) {
    // Network error (no response received)
    if (error.code === 'ERR_NETWORK') {
      errorMessage = 'Network error: Unable to connect to the server. Please check your internet connection.';
    } else if (error.code === 'ECONNABORTED') {
      errorMessage = 'Request timeout: The server took too long to respond.';
    } else {
      errorMessage = 'Network error: Unable to reach the server.';
    }
  } else if (error?.message) {
    // Standard error with message property
    if (error.message.includes('Network Error')) {
      errorMessage = 'Network error: Unable to connect to the server. Please check your internet connection.';
    } else {
      errorMessage = error.message;
    }
  } else if (typeof error === 'object' && error.msg) {
    errorMessage = error.msg;
  } else if (typeof error === 'object' && error.detail) {
    errorMessage = typeof error.detail === 'string' ? error.detail : JSON.stringify(error.detail);
  } else if (typeof error === 'string') {
    errorMessage = error;
  } else if (error?.code) {
    // Error with specific code
    switch (error.code) {
      case 'ERR_NETWORK':
        errorMessage = 'Network error: Unable to connect to the server. Please check your internet connection.';
        break;
      case 'ECONNABORTED':
        errorMessage = 'Request timeout: The server took too long to respond.';
        break;
      case 'ENOTFOUND':
        errorMessage = 'Network error: Unable to find the server. Please check the server address.';
        break;
      default:
        errorMessage = `Error (${error.code}): ${error.message || 'An unknown error occurred'}`;
    }
  } else if (error?.message && error.message.includes('ENOTFOUND')) {
    // Handle ENOTFOUND errors that don't have the code property
    errorMessage = 'Network error: Unable to find the server. Please check the server address.';
  }

  return errorMessage;
}