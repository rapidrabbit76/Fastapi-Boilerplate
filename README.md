# FastAPI Boilerplate

이 프로젝트는 확장 가능하고 유지보수하기 쉬운 FastAPI 애플리케이션을 빠르게 구축하기 위한 Cookiecutter 템플릿입니다. 모듈식 아키텍처, DDD(도메인 주도 설계) 개념 및 최신 Python 도구를 기반으로 합니다.

## ✨ 주요 특징

- **🚀 FastAPI 기반**: 현대적이고 빠른(고성능) 웹 프레임워크를 사용합니다.
- **🔩 모듈식 아키텍처**: `uv` 워크스페이스를 사용하여 프로젝트와 각 기능을 독립적인 패키지로 관리하여 결합도를 낮춥니다.
- **🧩 공유 커널(Shared Kernel)**: 여러 기능 모듈에서 공통적으로 사용되는 도메인 및 인프라 코드를 `shared_kernel`로 분리하여 일관성을 유지합니다.
- **🧱 계층형 설계**: 도메인, 인프라, 애플리케이션(유스케이스) 계층을 분리하여 관심사를 명확히 구분합니다.
- **📦 의존성 주입(DI)**: 컨테이너를 사용하여 의존성을 관리하고 테스트 용이성을 높입니다.
- **🛠️ 최신 개발 도구**: `uv`, `ruff`, `mypy`를 사용하여 개발 환경을 구성하고 코드 품질을 관리합니다.
- **🔑 인증**: `async-fastapi-jwt-auth`를 사용한 JWT 기반 인증을 지원합니다.
- **💾 데이터베이스**: SQLAlchemy 및 Alembic을 사용한 비동기 데이터베이스 작업을 지원합니다.
- **📡 비동기 통신**: `aio-pika` (RabbitMQ), `aioboto3` (AWS S3) 등 비동기 라이브러리를 사용하여 외부 서비스와 통신합니다.
- **🔭 Observability**: OpenTelemetry를 사용하여 분산 추적 및 로깅을 지원합니다.

## 🏗️ 프로젝트 구조

```
.
├── {{cookiecutter.project}}/      # uv 워크스페이스 루트
│   ├── pyproject.toml             # 워크스페이스 설정
│   ├── features/                  # 각 기능 모듈
│   │   ├── ...-shared_kernel      # 공통 도메인/인프라 로직
│   │   └── ...-shared_kernel-infra-* # 각 인프라 기술별 구현체
│   └── projects/                  # 실제 애플리케이션 프로젝트
│       └── ...-backend/           # FastAPI 백엔드 애플리케이션
│           ├── src/
│           └── pyproject.toml
└── cookiecutter.json              # 템플릿 변수 설정
```

## 🛠️ 기술 스택

- **웹 프레임워크**: FastAPI
- **개발/패키지 도구**: uv
- **코드 스타일/정적 분석**: Ruff, Mypy
- **데이터베이스**: SQLAlchemy, Alembic, PostgreSQL (psycopg2)
- **캐시**: Redis
- **메시지 큐**: RabbitMQ (aio-pika)
- **오브젝트 스토리지**: AWS S3 (aioboto3)
- **인증**: JWT (async-fastapi-jwt-auth)
- **Observability**: OpenTelemetry

## 🚀 시작하기

### 1. Cookiecutter로 프로젝트 생성하기

먼저 `cookiecutter`가 설치되어 있어야 합니다.

```bash
pip install cookiecutter
```

그 다음, 이 템플릿을 사용하여 새 프로젝트를 생성합니다.

```bash
cookiecutter gh:your-github-username/Fastapi-Boilerplate
```

프로젝트 이름, 설명 등 몇 가지 질문에 답변하면 템플릿으로부터 새 프로젝트가 생성됩니다.

### 2. 개발 환경 설정

생성된 프로젝트 폴더로 이동하여 `uv`를 사용해 가상 환경을 만들고 의존성을 설치합니다.

```bash
cd your-new-project-name
uv venv
source .venv/bin/activate
uv pip install -e .[dev]
```

### 3. 데이터베이스 마이그레이션

`alembic.ini` 파일에서 데이터베이스 설정을 확인하고 마이그레이션을 진행합니다.

```bash
cd projects/my-fastapi-project-backend
alembic upgrade head
```

### 4. 애플리케이션 실행

Uvicorn을 사용하여 FastAPI 애플리케이션을 실행합니다.

```bash
uvicorn my_fastapi_project.backend.main:app --reload --port 8000
```

이제 `http://127.0.0.1:8000/docs`로 접속하여 API 문서를 확인할 수 있습니다.
