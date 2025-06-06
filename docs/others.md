### 🔐 Informações sensíveis visíveis ou parcialmente mascaradas:

1. **`DB_HOST=***`**  
   - Isso já está mascarado, o que é ótimo. Certifique-se de que `DB_HOST` esteja armazenado como segredo no GitHub (`Settings > Secrets and variables > Actions`) e nunca hardcoded no YAML.

2. **`SENTRY_DNS=...`**  
   - Essa URL inclui uma **chave pública de projeto Sentry**, que embora não seja a chave secreta, ainda pode ser usada para identificar seu projeto ou permitir envio não autorizado de eventos. Considere movê-la para um **segredo**.

3. **`service_account: gha-service-account@agile-wheel.iam.gserviceaccount.com`**  
   - O nome do service account em si não é confidencial, mas se for usado com permissões sensíveis, evite expô-lo. Além disso, o uso de **`workload_identity_provider`** requer atenção redobrada para **não expor IDs de projeto GCP** e pools de identidade publicamente.

4. **`GITHUB_TOKEN` e `AUTHORIZATION: basic ***`**  
   - Essas credenciais estão mascaradas corretamente, mas **nunca devem ser reveladas** em logs completos.

5. **`/home/runner/.../gha-creds-xxxx.json`**  
   - Esse arquivo contém as credenciais temporárias para autenticação com GCP. Embora ele seja apagado no final, **nunca imprima seu conteúdo nem inclua-o em uploads ou logs visíveis.**

---

### ✅ Boas práticas já aplicadas:

- Credenciais estão mascaradas (`***`)
- `google-github-actions/auth` está usando `workload_identity_provider` (em vez de chave estática)
- Arquivos de credenciais são removidos após uso
- Token do GitHub não aparece em texto claro

---

### 📌 Recomendações adicionais:

1. **Use secrets para todas as variáveis sensíveis**, como:
   - `DB_HOST`, `DB_USER`, `DB_PASSWORD`
   - `SENTRY_DNS`
   - Qualquer chave de API, token de acesso, etc.

2. **Evite imprimir variáveis de ambiente sensíveis** usando `echo` ou `env` sem filtro.

3. **Revise permissões de `GITHUB_TOKEN` e do Service Account** — certifique-se de que têm o mínimo necessário.


### 📌 Ambiente de Produção atual
BackEnd: GCP - Cloud Run
FrontEnd: Vercel
DataBase: GCP - Firestore


### 📌 Variaveis de ambiente do backend tem que ser adiciona em:

- Arquivo de Settings
- Docker Compose
- env files
- Workflow de deploy
