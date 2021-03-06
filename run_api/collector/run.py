from datetime import datetime, timedelta, date
import time
import schedule
import argparse
import sys
from lib.config import LH_Api
from run_LH_announce import LHAnnounceRunner
from run_LH_result import LHResultRunner
from run_ETRI_result import ETRIResultRunner
from run_ETRI_announce import ETRIAnnounceRunner
from run_ETRI_cust import ETRICustRunner
from run_ETRI_cust_result import ETRICustResultRunner
import del_file
from lib.logger import Logger

class Runner():
    key = LH_Api.key

    default_begin = None
    default_end = None
    is_force = False

    def set_force_term(self, begin, end):
        self.default_begin = begin
        self.default_end = end
        self.is_force = True

    def get_term_info(self, name):
        return self.default_begin, self.default_end

    def run(self):
        # 개찰결과
        # if self.process_run(LHResultRunner) is False:
        #     return False
        # 입찰공고
        # if self.process_run(LHAnnounceRunner) is False:
        #     return False
        # # 결과
        if self.process_run(ETRIResultRunner) is False:
            return False
        # # # 입찰공고
        if self.process_run(ETRIAnnounceRunner) is False:
            return False
        # # # 견적요청
        if self.process_run(ETRICustRunner) is False:
            return False
        # # 견적결과
        if self.process_run(ETRICustResultRunner) is False:
            return False

    def process_run(self, cls, term_days=0):
        name = cls.__name__

        begin, end = self.get_term_info(name)

        if self.is_force is False and term_days > 0:
            begin_date = datetime.strptime(begin, '%Y%m%d%H%M').strftime('%Y%m%d')
            end_date = (datetime.strptime(end, '%Y%m%d%H%M') - timedelta(days=term_days)).strftime('%Y%m%d')

            if begin_date <= end_date:
                self.logger.debug(f'start: {name}, begin({begin}), end({end}), term_days({term_days})')

                runner = cls(self.key, begin, end)
                if runner.exec() is False:
                    self.logger.error(f'failed: {name}')
                    return False

                self.logger.debug(f'finish: {name}')
            else:
                self.logger.debug(f'skip: {name}, begin({begin_date}), end({end_date}), term_days({term_days})')
        else:
            runner = cls(self.key, begin, end)
        if runner.exec() is False:
            return False

def schedule_run():
    now = date.today()
    end_d = date.today() + timedelta(10)
    runner = Runner()
    runner.set_force_term(now.strftime("%Y%m%d"), end_d.strftime("%Y%m%d"))
    runner.run()

def del_schedule_run():
    # 한번 가져오고
    schedule_run()
    # 마지막 삭제
    time = date.today() - timedelta(1)
    # 1:입찰공고 2:개찰결과 3:견적문의 4:견적결과
    del_file.del_db_old_line(1,time)
    del_file.del_db_old_line(2,time)
    del_file.del_db_old_line(3,time)
    del_file.del_db_old_line(4,time)


# 30분 단위로 실행
schedule.every(30).minutes.do(schedule_run)
schedule.every().day.at("00:30").do(del_schedule_run)

if __name__ == '__main__':
    #인자 넣어주기
    parser = argparse.ArgumentParser()
    #시작 끝 넣기   (년 월 일) <- LH   
    # 디포트값 수정
    parser.add_argument('--begin', required=True, help='yyyyMMdd')
    parser.add_argument('--end', required=True, help='yyyyMMdd')
    #인자 받아오기
    args = parser.parse_args()

    try:
        #시간 가져오기  (년 월 일 시간 분)
        datetime.strptime(args.begin, '%Y%m%d')
        datetime.strptime(args.end, '%Y%m%d')
    except (TypeError, ValueError):
        parser.print_usage()
        sys.exit()

    runner = Runner()
    runner.set_force_term(args.begin, args.end)
    runner.run()

    while True:
        schedule.run_pending()
        time.sleep(1)
