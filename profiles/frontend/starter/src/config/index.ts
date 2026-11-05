import { z } from 'zod';

const envSchema = z.object({
  VITE_API_BASE_URL: z.string().url().default('http://localhost:8000/api/v1'),
  VITE_APP_NAME: z.string().default('Universal AI-Native App'),
  VITE_ENABLE_MOCK: z.string().optional().default('false'),
});

const rawEnv = {
  VITE_API_BASE_URL: import.meta.env.VITE_API_BASE_URL,
  VITE_APP_NAME: import.meta.env.VITE_APP_NAME,
  VITE_ENABLE_MOCK: import.meta.env.VITE_ENABLE_MOCK,
};

export const env = envSchema.parse(rawEnv);
