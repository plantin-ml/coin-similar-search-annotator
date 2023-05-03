import json
import os
from pathlib import Path

# import fiftyone as fo
import mysql.connector
import pandas as pd
from api.const.common import AnnotationJobType, AnnotationTaskType
from api.core.config import get_app_settings
from api.schemas.jobs import AnnotationJob
from api.services.jobs import AnnotationJobsService
from api.services.tasks import AnnotationTasksService
from tqdm.auto import tqdm

settings = get_app_settings()


class TasksCreator():
    task_service: AnnotationTasksService = AnnotationTasksService()
    job_service: AnnotationJobsService = AnnotationJobsService()

    async def create_from_fiftyone(self, job_alias: str):
        pass
        # dataset = fo.load_dataset('coin-user-images')

        # data_view = dataset.match_tags("ann_images_for_emb")
        # await self.job_service.create_job(AnnotationJob(
        #     alias=job_alias,
        #     state='draft',
        #     name=job_alias,
        #     user_assignee='admin',
        #     job_type='user_images',
        # ))

        # for i, sample in enumerate(data_view.iter_samples(progress=True)):
        #     filename = sample.filepath.split('/')[-1]

        #     await self.task_service.create_task(
        #         url=os.path.join(settings.retrieve_gallery_images_base_url, filename),
        #         task_alias='{}'.format(sample.id),
        #         coin_side='none',
        #         tags=[],
        #         job_alias=job_alias,
        #         task_type=AnnotationTaskType.user_images,
        #     )

    async def create_from_csv(
        self,
        task_alias_prefix: str,
        job_alias: str,
        task_type: str,
        csv_file: Path
    ):
        await self.job_service.create_job(AnnotationJob(
            alias=job_alias,
            state='draft',
            name=job_alias,
            user_assignee='admin',
            job_type=AnnotationJobType.gallery_images,
        ))

        data_df = pd.read_csv(
            csv_file,
            usecols=[
                'coin_id',
                'original_url',
                'coin_side',
                'file_name',
                'name',
                'country',
                'denomination',
                'year',
                'coin_type'
            ])

        for _, row in tqdm(data_df.iterrows()):
            await self.task_service.create_task_from_dict(
                job_alias=job_alias,
                task_alias=f"{task_alias_prefix}-{row['coin_id']}",
                task_type=task_type,
                data=row.to_dict()
            )

    async def process(self):
        job_alias = 'coin-from-db-part-8'
        await self.job_service.create_job(AnnotationJob(
            alias=job_alias,
            state='draft',
            name=job_alias,
            user_assignee='andriy',
            job_type=AnnotationJobType.gallery_images,
        ))
        db = mysql.connector.connect(
            host=settings.mysql_host,
            user=settings.mysql_user,
            password=settings.mysql_password,
            database=settings.mysql_database
        )
        cursor = db.cursor()
        query = "SELECT `id`, `image_url` FROM user_identifications WHERE `id` < 44239 ORDER BY `id` DESC LIMIT 500 OFFSET 1500"
        cursor.execute(query)

        for row in tqdm(cursor.fetchall()):
            task_id = int(row[0])
            urls = json.loads(row[1])

            for i, url in enumerate(urls):
                await self.task_service.create_task(
                    url=url,
                    task_alias=f"{job_alias}-{task_id}-{i}",
                    coin_side='obverse' if i == 0 else 'reverse',
                    job_alias=job_alias,
                    task_type=AnnotationTaskType.user_images,

                )

    async def from_csv(self, csv_file: Path):
        data_df = pd.read_csv(
            csv_file,
            usecols=[
                'coin_id',
                'original_url',
                'coin_side',
                'file_name',
                'name',
                'country',
                'denomination',
                'year',
                'coin_type'
            ])

        for idx, row in tqdm(data_df.iterrows()):
            await self.task_service.create_task_from_dict(task_alias=f"usa-obverse-{idx}", data=row.to_dict())




