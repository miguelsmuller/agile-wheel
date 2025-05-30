import fs from 'fs';
import dotenv from 'dotenv';
import dotenvExpand from 'dotenv-expand';

if (fs.existsSync('.env')) {
  const env = dotenv.config();
  dotenvExpand.expand(env);
} else {
  console.warn('⚠️  .env file not found. Skipping...');
}

const content = `// This file is automatically generated by the build script
export const environment = {
  production: ${process.env.PRODUCTION === 'true'},
  apiAgileWheelUrl: '${process.env.API_AGILEWHEEL_URL}',
  wsAgileWheelUrl: '${process.env.WS_AGILEWHEEL_URL}',
};
`;

fs.writeFileSync('src/environments/environment.ts', content);

console.log('✅ environment.ts has been successfully generated!');
