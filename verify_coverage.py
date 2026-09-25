import os
import re
import sys

def verify_coverage():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(base_dir, "src")
    syllabus_path = os.path.join(base_dir, "syllabus.md")
    
    if not os.path.exists(syllabus_path):
        print(f"Error: {syllabus_path} not found.")
        sys.exit(1)
        
    with open(syllabus_path, "r", encoding="utf-8") as f:
        syllabus_content = f.read()

    # Collect all official doc topic files
    doc_topics = []
    for root, dirs, files in os.walk(src_dir):
        dirs.sort()
        for f in sorted(files):
            if f.endswith("_en.md") and not f.startswith("documentation_") and not f.startswith("license_") and not f.startswith("readme_"):
                group_dir = os.path.basename(root)
                slug = f[:-6]
                rel_path = f"{group_dir}/{slug}"
                doc_topics.append({
                    "group": group_dir,
                    "slug": slug,
                    "en_file": f"{slug}_en.md",
                    "ko_file": f"{slug}_ko.md",
                    "rel_path": rel_path
                })

    total_docs = len(doc_topics)
    matched = []
    missing = []

    for item in doc_topics:
        slug = item["slug"]
        ko_file = item["ko_file"]
        # Check if the slug or ko file is mentioned in syllabus.md
        pattern = re.compile(rf"\b{re.escape(slug)}(_ko\.md|_en\.md|\.md)?\b|/{re.escape(slug)}", re.IGNORECASE)
        m = pattern.search(syllabus_content)
        if m:
            matched.append(item)
        else:
            missing.append(item)

    coverage_rate = (len(matched) / total_docs) * 100 if total_docs > 0 else 0
    
    print("=" * 65)
    print(" 🔍 라라벨 공식 문서 전수 포함율 검증 리포트 (Full Coverage Report)")
    print("=" * 65)
    print(f" • 총 공식 문서 주제 수 : {total_docs}개 (11개 전체 그룹)")
    print(f" • 실습 계획 매핑 문서 수 : {len(matched)}개")
    print(f" • 미매핑 문서 수         : {len(missing)}개")
    print(f" • 공식 문서 커버리지     : {coverage_rate:.1f}%")
    print("-" * 65)

    if missing:
        print("⚠️ 누락된 문서 목록:")
        for m in missing:
            print(f"   - [{m['group']}] {m['slug']} ({m['ko_file']})")
        print("-" * 65)
        print("❌ 100% 매핑에 도달하지 못했습니다.")
        return False
    else:
        print("✅ 100% 전수 매핑 확인 완료!")
        print("   공식 문서의 모든 주제가 14주 핸드온 쇼핑몰 커리큘럼에 완벽히 포함되어 있습니다.")
        print("=" * 65)
        return True

if __name__ == "__main__":
    verify_coverage()
