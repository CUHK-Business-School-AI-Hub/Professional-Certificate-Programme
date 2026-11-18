# API Access Guide source

`build_guide.py` creates `../../guides/API Access Guide.pdf`, a four-page English illustrated handout. Run it with Python and ReportLab. It reads the existing course HTML for the school logo and uses the local official screenshot below. Paths are relative to this source directory; the build does not need a network request.

## Verified sources

OpenAI credit benefit rechecked 18 November 2026; other illustrations and provider setup sources originally checked 17 November 2026:

- [OpenAI API credit benefit](https://help.openai.com/en/articles/20001626-api-credits-benefit-for-eligible-chatgpt-subscriptions): seven-day paid-subscription eligibility, account linking, claim flow and expiry.
- [OpenAI projects and API keys](https://help.openai.com/en/articles/9186755-managing-projects-in-the-api-platform): project selection and key creation. `openai-api-keys.webp` is the article's official annotated illustration, not a screenshot of the user's account. [Image URL](https://images.ctfassets.net/j22is2dtoxu1/intercom-img-e0b10057112edb4f7ffd81c0/3b9fb08bcc636eaefee1a7f6c5391ea2/Frame_12.png?fm=webp&q=80&w=1344).
- [OpenAI key handling](https://developers.openai.com/api/docs/guides/api-keys): local-development credentials and server-side secret storage.
- [DeepSeek Help Center](https://static.deepseek.com/faq/index.html?lang=en): browser inspection of API > How to Top Up? confirmed the Top Up and Billing page names and listed payment methods (PayPal, bank card, Alipay, WeChat Pay).
- [DeepSeek first call](https://api-docs.deepseek.com/): platform/API-key link and environment-variable pattern.
- [DeepSeek balance API](https://api-docs.deepseek.com/api/get-user-balance/): balances use CNY or USD.
- [DeepSeek error codes](https://api-docs.deepseek.com/quick_start/error_codes/): authentication, insufficient balance and rate-limit errors.

The recommended starting budget of approximately HK$10 is the instructor's course guidance. Public sources did not establish the current minimum top-up or the checkout options for a particular account. The handout therefore tells learners to check the checkout currency and total, and to consult the TA if the minimum exceeds that budget.

Navigation diagrams are labelled as illustrative. The DeepSeek authenticated console returned 403 during preparation; no live console screenshot or completed purchase is claimed. No API key was created and no paid test was run in preparing this guide.

PDF rendering and visual QA outputs belong in the ignored `build/api-access-guide/` directory.
