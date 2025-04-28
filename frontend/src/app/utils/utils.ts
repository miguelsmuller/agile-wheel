export function parseJSON<T>(jsonString: string): T {
    try {
      return JSON.parse(jsonString) as T;
    } catch (error) {
      throw new Error('Invalid JSON format');
    }
  }