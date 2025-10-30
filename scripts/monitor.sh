#!/bin/bash

# MGNREGA Dashboard - Monitoring Script
# Checks health of all services and displays status

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

clear

echo "╔════════════════════════════════════════════════════════════╗"
echo "║       MGNREGA Dashboard - System Monitor                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Function to check service
check_service() {
    local service_name=$1
    local check_command=$2
    
    if eval $check_command > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $service_name is ${GREEN}HEALTHY${NC}"
        return 0
    else
        echo -e "${RED}✗${NC} $service_name is ${RED}DOWN${NC}"
        return 1
    fi
}

# Check Docker
echo "━━━ Docker Services ━━━"
if docker info > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Docker daemon is ${GREEN}RUNNING${NC}"
else
    echo -e "${RED}✗${NC} Docker daemon is ${RED}NOT RUNNING${NC}"
    exit 1
fi

# Check containers
echo ""
echo "━━━ Container Status ━━━"
docker-compose ps --format "table {{.Service}}\t{{.Status}}" 2>/dev/null || {
    echo -e "${RED}✗${NC} Could not get container status"
}

# Check individual services
echo ""
echo "━━━ Service Health ━━━"
check_service "Backend API      " "curl -f http://localhost:8000/api/v1/health"
check_service "Frontend         " "curl -f http://localhost:3000"
check_service "PostgreSQL       " "docker-compose exec -T db pg_isready -U postgres"
check_service "Redis            " "docker-compose exec -T redis redis-cli ping"

# Check disk usage
echo ""
echo "━━━ Resource Usage ━━━"
DISK_USAGE=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -lt 80 ]; then
    echo -e "${GREEN}✓${NC} Disk Usage: ${DISK_USAGE}% ${GREEN}(OK)${NC}"
elif [ $DISK_USAGE -lt 90 ]; then
    echo -e "${YELLOW}⚠${NC} Disk Usage: ${DISK_USAGE}% ${YELLOW}(WARNING)${NC}"
else
    echo -e "${RED}✗${NC} Disk Usage: ${DISK_USAGE}% ${RED}(CRITICAL)${NC}"
fi

# Check memory
MEMORY_USAGE=$(free | grep Mem | awk '{print int($3/$2 * 100)}')
if [ $MEMORY_USAGE -lt 80 ]; then
    echo -e "${GREEN}✓${NC} Memory Usage: ${MEMORY_USAGE}% ${GREEN}(OK)${NC}"
elif [ $MEMORY_USAGE -lt 90 ]; then
    echo -e "${YELLOW}⚠${NC} Memory Usage: ${MEMORY_USAGE}% ${YELLOW}(WARNING)${NC}"
else
    echo -e "${RED}✗${NC} Memory Usage: ${MEMORY_USAGE}% ${RED}(CRITICAL)${NC}"
fi

# Check database size
echo ""
echo "━━━ Database Stats ━━━"
DB_SIZE=$(docker-compose exec -T db psql -U postgres -d mgnrega -t -c "SELECT pg_size_pretty(pg_database_size('mgnrega'));" 2>/dev/null | xargs)
if [ ! -z "$DB_SIZE" ]; then
    echo -e "${BLUE}ℹ${NC} Database Size: ${DB_SIZE}"
fi

STATES_COUNT=$(docker-compose exec -T db psql -U postgres -d mgnrega -t -c "SELECT COUNT(*) FROM states;" 2>/dev/null | xargs)
DISTRICTS_COUNT=$(docker-compose exec -T db psql -U postgres -d mgnrega -t -c "SELECT COUNT(*) FROM districts;" 2>/dev/null | xargs)
METRICS_COUNT=$(docker-compose exec -T db psql -U postgres -d mgnrega -t -c "SELECT COUNT(*) FROM monthly_metrics;" 2>/dev/null | xargs)

if [ ! -z "$STATES_COUNT" ]; then
    echo -e "${BLUE}ℹ${NC} States: ${STATES_COUNT} | Districts: ${DISTRICTS_COUNT} | Metrics: ${METRICS_COUNT}"
fi

# Check Redis
echo ""
echo "━━━ Cache Stats ━━━"
REDIS_KEYS=$(docker-compose exec -T redis redis-cli DBSIZE 2>/dev/null | grep -oE '[0-9]+')
if [ ! -z "$REDIS_KEYS" ]; then
    echo -e "${BLUE}ℹ${NC} Redis Keys: ${REDIS_KEYS}"
fi

# Check logs for errors
echo ""
echo "━━━ Recent Errors ━━━"
ERROR_COUNT=$(docker-compose logs --tail=100 2>/dev/null | grep -i "error\|exception\|failed" | wc -l)
if [ $ERROR_COUNT -eq 0 ]; then
    echo -e "${GREEN}✓${NC} No errors in recent logs"
else
    echo -e "${YELLOW}⚠${NC} Found ${ERROR_COUNT} errors in recent logs"
    echo -e "   Run: ${BLUE}docker-compose logs | grep -i error${NC} to view"
fi

# Access URLs
echo ""
echo "━━━ Access URLs ━━━"
echo -e "${BLUE}Frontend:${NC}  http://localhost:3000"
echo -e "${BLUE}Backend:${NC}   http://localhost:8000"
echo -e "${BLUE}API Docs:${NC}  http://localhost:8000/api/docs"

# Last update
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "Last updated: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
