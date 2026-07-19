> 이 문서는 이중 언어 문서입니다. 각 섹션에서 영어 원문이 먼저 나오고, **[한국어]** 표시 아래에 한국어 번역이 이어집니다.

> 원본: docs/SPONSORS.md @ 6aa15f6504ce782e9d42af61512582f26c2ed846

# Sponsors (스폰서)

This document defines how sponsor logos are added to the OpenMontage README.

**[한국어]**

이 문서는 OpenMontage README에 스폰서 로고를 추가하는 방법을 정의하는 문서입니다.

---

## Sponsor Asset Convention (스폰서 에셋 규칙)

- Store sponsor logos in `assets/sponsors/`.
- Use a lowercase kebab-case filename based on the sponsor name, for example `acme-video.svg`.
- Prefer SVG. Use PNG only when the sponsor cannot provide vector artwork.
- Keep logos transparent, tightly cropped, and readable at `44px` height.
- Use the sponsor's official website or product page as the link target.
- Use descriptive alt text: `Acme Video logo`, not just `logo`.

**[한국어]**

- 스폰서 로고는 `assets/sponsors/`에 저장합니다.
- 스폰서 이름을 기준으로 소문자 케밥 케이스 파일 이름을 사용합니다. 예: `acme-video.svg`
- SVG를 우선 사용합니다. 스폰서가 벡터 아트워크를 제공할 수 없을 때만 PNG를 사용합니다.
- 로고는 투명하게, 잘린 여백을 최소화하고, `44px` 높이에서 읽기 쉽게 유지합니다.
- 링크 대상은 스폰서의 공식 웹사이트 또는 제품 페이지로 합니다.
- 설명적인 대체 텍스트를 사용합니다: `logo`가 아니라 `Acme Video logo`처럼 구체적으로 작성합니다.

---

## README Snippet (README 스니펫)

Add each sponsor as a table row inside the `Sponsors` section near the top of `README.md`:

```html
<tr>
<td width="180" align="center"><a href="https://example.com"><img src="assets/sponsors/example-sponsor.svg" alt="Example Sponsor" width="150"></a></td>
<td><strong>Example Sponsor</strong> helps OpenMontage users do something concrete. Mention the useful product outcome, then close with a short <a href="https://example.com">CTA link</a>.</td>
</tr>
```

For a sponsor with separate light and dark logos, use a `picture` element:

```html
<tr>
<td width="180" align="center">
  <a href="https://example.com">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/sponsors/example-sponsor-dark.svg">
      <img src="assets/sponsors/example-sponsor-light.svg" alt="Example Sponsor" width="150">
    </picture>
  </a>
</td>
<td><strong>Example Sponsor</strong> helps OpenMontage users do something concrete. Mention the useful product outcome, then close with a short <a href="https://example.com">CTA link</a>.</td>
</tr>
```

**[한국어]**

각 스폰서는 `README.md` 상단의 `Sponsors` 섹션 안에 테이블 행으로 추가합니다. 위의 HTML 예제를 참고하여 스폰서 정보를 입력합니다.

밝은 모드와 어두운 모드용 로고를 별도로 제공하는 스폰서의 경우 `picture` 요소를 사용합니다. 위의 두 번째 HTML 예제를 참고하여 구현합니다.

---

## Intake Checklist (입력 체크리스트)

Before adding a sponsor, collect:

- Sponsor display name
- Sponsor URL
- Logo file, preferably SVG
- Confirmation that OpenMontage has permission to display the logo in the README
- Any required trademark wording, if the sponsor has one

Do not add tracking URLs, affiliate redirects, or claims about endorsement unless they are explicitly approved by the project maintainer.

**[한국어]**

스폰서를 추가하기 전에 다음 정보를 수집합니다.

- 스폰서 표시 이름
- 스폰서 URL
- 로고 파일(우선 SVG)
- OpenMontage가 README에 로고를 표시할 권한이 있다는 확인
- 스폰서가 요구하는 상표 문구가 있는 경우 해당 내용

프로젝트 관리자가 명시적으로 승인하지 않은 한 추적 URL, 제휴 리디렉션, 보증에 대한 주장을 추가하지 않습니다.
